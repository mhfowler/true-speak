from django.http import HttpResponse, HttpResponseNotAllowed
from django import shortcuts
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from truespeak.models import *
from truespeak.common import sendEmailAssociationConfirmation, getNewConfirmationLink
import json, random
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


# authentication backends
from socialregistration.contrib.facebook.models import FacebookProfile

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
    return render_to_response('home.html',locals())

def goodbye(request):
    return render_to_response('goodbye.html',locals())

def welcome(request):
    return render_to_response('welcome.html',locals())

def about(request):
    return render_to_response('docs.html',locals())

def contact(request):
    return render_to_response('contact.html',locals())

def settingsPage(request):
    user = request.user
    # if its a post then user is updating some settings
    if request.method == "POST":
        to_return = {
            "error":None,
            "message":""
        }
        if "new_email" in request.POST:
            new_email = request.POST['new_email']
            already = EmailProfile.objects.filter(email=new_email)
            if already:
                email_profile = already[0]
                if email_profile.confirmed:
                    to_return["error"] = "This email address is already associated with a ParselTongue user."
                else:
                    email_profile.user = user
                    email_profile.confirmation_link = getNewConfirmationLink()
                    email_profile.save()
                    sendEmailAssociationConfirmation(email_profile)
                    to_return["message"] = "A confirmation email has been resent to your email address."
            else:
                email_profile = EmailProfile(email=new_email, user=user, confirmed=False)
                email_profile.confirmation_link = getNewConfirmationLink()
                email_profile.save()
                sendEmailAssociationConfirmation(email_profile)
                to_return["message"] = "A confirmation email has been sent to your email address."

        # return json
        return HttpResponse(json.dumps(to_return), content_type="application/json")

    # otherwise we are just displaying settings
    else:
        associated_email_addresses = getAssociatedEmailAddresses(user, confirmed=True)
        return render_to_response('settings.html',locals())

def confirmEmail(request, link_number):
    email_profile = EmailProfile.objects.filter(confirmation_link=link_number)
    if not email_profile:
        return HttpResponse("There is no email profile at this link.")
    # TODO: check if confirmation link is less than 2 weeks old
    email_profile = email_profile[0]
    user = request.user
    if not email_profile.confirmed:
        email_profile.user = user
        email_profile.confirmed = True
        email_profile.save()
        return shortcuts.redirect("/settings/")
    else:
        return shortcuts.redirect("/settings/")



def loginPage(request):
    if request.method == "GET":
        return render_to_response('login.html',locals(), context_instance=RequestContext(request))
    else:
        email = request.POST['email']
        password = request.POST['password']
        error = ""
        try:
            email_profile = EmailProfile.objects.get(email=email)
        except ObjectDoesNotExist:
            error = "Oops, this email was not found. <br> Try <a href='/register/'>registering?</a>"
        except MultipleObjectsReturned:
            print ("shit this should never happen.")
        else:
            if not email_profile.confirmed:
                error = "Oops, this email has not been confirmed. <br> <a href='/reconfirm/" + email + "/'> Resend? </a>"
            else:
                user = email_profile.user
                user = authenticate(username=user.username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                    else:
                        error = "Your account has been disabled!"
                else:
                    error = "Oops, email/password was not found."
        to_return = {
            "error":error,
            "message":"blah"
        }
        return HttpResponse(json.dumps(to_return), content_type="application/json")



def registerPage(request):
    if request.method == "GET":
        return render_to_response('register.html',locals(), context_instance=RequestContext(request))
    else:
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        error = ""
        if not password1:
            error = "Oops, password can't be empty."
        elif not password1 == password2:
            error = "Oops, passwords must be the same."
        # check if email already exists
        already = EmailProfile.objects.filter(email=email, confirmed=True)
        if already:
            error = "This email is already associated with an account.<br> Try <a href='/login/'>logging in?</a>"
        if not error:
            user = User.objects.create_user(username=email, email=email, password=password1)
        to_return = {
            "error":error,
            "message":"blah"
        }
        return HttpResponse(json.dumps(to_return), content_type="application/json")


def errorView(request, error_dict=None):
    return HttpResponse("My special error view.")




# list of identifiers which can be used to find associated public keys
ALLOWED_IDENTIFIERS = ["email"]

def getPubKeys(request):
    """
        If requested_keys in request.POST:
            Returns JSON list of pubkey/username data associated with each identifier dict in requested_keys.
        Else:
            Returns single pubkey/username data, treating entire request.POST as identifier dict.
        Each identifier must be a dictionary of identifier:value meant to identify a user.
        Format of response for each identifier_dict is described under getPubkeysAssociatedWithIndentifiers
    """
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    requested_keys = request.POST.get('requested_keys')
    # if post is list of identifier dict
    if requested_keys:
        to_return = []
        for identifier_dict in requested_keys:
            result = getPubKeysAssociatedWithIndentifiers(identifier_dict)
            to_return.append(result)
    # else assuming post is single identifier dict
    else:
        to_return = getPubKeysAssociatedWithIndentifiers(request.POST)

    # return json
    return HttpResponse(json.dumps(to_return), content_type="application/json")


def getPubKeysAssociatedWithIndentifiers(identifier_dict):
    """
        identifier_dict must be a dictionary of identifier:value meant to identify a user.
        Returns dictionary:
         'identifier_used': None if does not exist, string of the identifier that was used if user was found
         'error': Error message if there was a problem, None if query was successful
         'pub_keys': None if does not exist, otherwise list of pub_key strings
         'username': None if does not exist, otherwise parseltongue username associated with pub_keys
    """

    to_return = {}
    to_return["identifier_used"] = identifier_used = None
    to_return["error"] = error = None
    to_return["pub_keys"] = None
    to_return["username"] = None
    user = None

    # for all identifier,values to try... give it a go
    # TODO: should we check if there are conflicting results by different identifiers?
    for identifier,value in identifier_dict.items():

        if identifier == "facebook_id":
            fb_id = value
            try:
                fb_profile = FacebookProfile.objects.get(uid=fb_id)
                user = fb_profile.user
                identifier_used = identifier
                break
            except ObjectDoesNotExist:
                continue
            except Exception as e:
                error = e.message
                break

        if identifier == "email":
            email = value
            try:
                email_profile = EmailProfile.objects.get(email=email)
                user = email_profile.user
                identifier_used = identifier
            except ObjectDoesNotExist:
                continue
            except Exception as e:
                error = e.message
                break

    to_return["error"] = error # this will still be none if there were no errors
    if identifier_used: # this means a user was found
        pub_keys = getUserPubKeys(user)
        username = user.username
        to_return["identifier_used"] = identifier_used
        to_return["pub_keys"] = pub_keys
        to_return["username"] = username

    return to_return


def uploadPubKey(request):
    """
    Upload a pub key to your user account.
    """
    user = request.user
    pub_key_text = request.POST['pub_key']
    prior_keys = PubKey.objects.filter(user=user)
    if prior_keys:
        pass
        # TODO: should send you an email saying a pub_key was uploaded to your account, if not initial registration
    already = PubKey.objects.filter(user=user,pub_key_text=pub_key_text)
    if not already:
        pub_key = PubKey(user=request.user, pub_key_text=pub_key_text)
        pub_key.save()
        return HttpResponse("Success")
    else:
        return HttpResponse("Error: Key has already been uploaded.")


def uploadPriKey(request):
    """
    Upload an encrypted private key to your user account.
    """
    user = request.user
    pri_key_text = request.POST['pri_key']
    already = PriKey.objects.get_or_none(user=user)
    if already:
        already.pri_key_text = pri_key_text
        already.save()
    else:
        pri_key = PriKey(user=user, pri_key_text=pri_key_text)
        pri_key.save()
    return HttpResponse("Success")










