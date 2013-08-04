from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django import shortcuts
from truespeak.models import *

from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response

import json

import settings

from helpers.facebook import *

# ==========================================================
# BOILERPLATE
# ==========================================================

def redirect(request, page='/home'):
    return shortcuts.redirect(page)

def viewWrapper(view):
    def new_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponse("You need to be logged in doe")
        else:
            return view(request,*args,**kwargs)
    return new_view


def home(request):
    return HttpResponse("hello world")


# ==========================================================
# FACEBOOK LOGIN
# ==========================================================

def channel(request):
    return render_to_response('channel.html',locals())

def connect_with_facebook(request):
    
    MEDIA_URL = settings.MEDIA_URL
    PAGE_TITLE = "Connect TrueSpeak with Facebook"
    
    # return render_to_response('connect_with_facebook_bootstrap.html',locals())
    return render_to_response('connect_with_facebook.html',locals())

def facebook_callback(request):
    """
        If token is for user in existing account, log them in.
        Otherwise, create the user and log them in.
    """ 

    oauth_access_token = request.GET["token"]
    
    graph = GraphAPI(oauth_access_token)
    results = graph.request("me")

    fb_id = results["id"]

    try:
        user = User.objects.get(username = fb_id)
        profile = user.get_profile()
    except User.DoesNotExist:
        
        # ensure there's a facebook_user for this
        try:
            facebook_user = Facebook_User.objects.get(fb_id = fb_id)
        except Facebook_User.DoesNotExist:
            facebook_user = Facebook_User()
            facebook_user.fb_id = fb_id
            facebook_user.handle = results["username"]
            facebook_user.first_name = results["first_name"]
            facebook_user.last_name = results["last_name"]
            facebook_user.save()

        user = User.objects.create_user(fb_id, "blank@facebook.com", fb_id)
        user.save()

        profile = user.get_profile()
        profile.facebook_user = facebook_user
        profile.save()

        # import the user's friends
        results = graph.request("%s/friends" % user.username, args = {'fields' : 'first_name,last_name,username'})
        for result in results['data']:
            
            # ensure this friend exists in Facebook_User
            try:
                fbuser = Facebook_User.objects.get(fb_id = result["id"])
            except Facebook_User.DoesNotExist:
                fbuser = Facebook_User()
                fbuser.fb_id = result["id"]
                try:
                    fbuser.handle = result["username"]
                except:
                    fbuser.handle = ""
                fbuser.first_name = result["first_name"]
                fbuser.last_name = result["last_name"]
                fbuser.save()
            
            profile.friends.add(fbuser)

        # create a plugin token to authenticate later with
        import hashlib, datetime
        m = hashlib.md5()
        m.update(str(datetime.datetime.now()))
        
        profile.plugin_token = m.hexdigest()

        profile.save()

    user = authenticate(username=fb_id, password=fb_id)
    login(request, user)
            
    return HttpResponse(fb_id)

def done_token(request):

    user = request.user
    profile = user.get_profile()

    plugin_token = profile.plugin_token
    fb_id = user.username
    fb_handle = profile.facebook_user.handle

    return render_to_response('done_token.html',locals())

def upload_pubkey(request):

    try:
        user = User.objects.get(userprofile__plugin_token = request.GET["auth_token"])
        profile = user.get_profile()
    except:
        response = {"Error":"Not authenticated"}
        return HttpResponse(json.dumps(response), content_type="application/json")

    pubkeys = json.loads(profile.pubkeys)
    pubkeys.append(request.GET["key"])
    profile.pubkeys = json.dumps(pubkeys)
    profile.save()

    return HttpResponse("Success")

def friends(request):

    try:
        user = User.objects.get(userprofile__plugin_token = request.GET["auth_token"])
        profile = user.get_profile()
    except:
        response = {"Error":"Not authenticated"}
        return HttpResponse(json.dumps(response), content_type="application/json")

    # only include friends who are on the platform in the response
    response = {"friends":{}}
    for FBfriend in profile.friends.all():
       
        # check if user on platform
        friend = False
        try:
            friend = User.objects.get(username = FBfriend.fb_id)
        except User.DoesNotExist:
            pass

        if friend:
            friend_profile = friend.get_profile()

            friendDict = {}
            friendDict["name"] = "%s %s" % (friend_profile.facebook_user.first_name, friend_profile.facebook_user.last_name)
            friendDict["pub_keys"] = json.loads(friend_profile.pubkeys)
            friendDict["fb_id"] = friend.username
            friendDict["fb_handle"] = friend_profile.facebook_user.handle
            response["friends"][friend.username] = friendDict

    # per Josh's request, add yourself as one of the friends
    friendDict = {}
    friendDict["name"] = "%s %s" % (profile.facebook_user.first_name, profile.facebook_user.last_name)
    friendDict["pub_keys"] = json.loads(profile.pubkeys)
    friendDict["fb_id"] = user.username
    friendDict["fb_handle"] = profile.facebook_user.handle
    response["friends"][user.username] = friendDict

    return HttpResponse(json.dumps(response), content_type="application/json")


