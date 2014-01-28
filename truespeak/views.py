from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django import shortcuts
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from truespeak.common import sendEmailAssociationConfirmation, getNewConfirmationLink, logError, createEmailProfile, normalize_email, _template_values
from truespeak.models import *
from django.conf import settings
from annoying.decorators import render_to

import json


def redirect(request, page='/home'):
    return shortcuts.redirect(page)


def json_response(res):
    return HttpResponse(json.dumps(res), 
        content_type="application/json")


def viewWrapper(view):
    @csrf_exempt
    def new_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return shortcuts.redirect("/login/")
        else:
            return view(request, *args, **kwargs)
    return new_view


def home(request):
    if request.user.is_authenticated():
        return shortcuts.redirect("/settings/")
    return _template_values('home.html', locals(), 
        context_instance=RequestContext(request))


@render_to("welcome.html")
def welcome(request, email_address=None):
    return _template_values(request, page_title="welcome", 
        email_address=email_address)


@render_to("about.html")
def about(request):
    return _template_values(request, page_title="about", 
        navbar="nav_about")


@render_to("tutorial.html")
def tutorial(request):
    return _template_values(request, page_title="tutorial")


@render_to("team.html")
def team(request):
    return _template_values(request, page_title="team", 
        navbar="nav_team")


@render_to("initializing.html")
def initializingPage(request):
    return _template_values(request, page_title="initializing")


@ensure_csrf_cookie
def settingsPage(request):
    user = request.user
    # if its a post then user is updating some settings
    if request.method == "POST":
        to_return = {
            "error": None,
            "message": ""
        }
        if "new_email" in request.POST:
            new_email = normalize_email(request.POST['new_email'])
            success, message = createEmailProfile(new_email, user)
            if success:
                to_return['message'] = message
            else:
                to_return['error'] = message
        elif "delete_email" in request.POST:
            delete_email = normalize_email(request.POST['delete_email'])
            success = removeEmailAddress(delete_email, user)
            if not success:
                to_return['error'] = True
        return json_response(to_return)

    # otherwise we are just displaying settings
    else:
        associated_email_addresses = getAssociatedEmailAddresses(user)
        return render_to_response('settings.html', locals())


def confirmEmail(request, link_number):
    email_profile = EmailProfile.objects.filter(confirmation_link=link_number)
    if not email_profile:
        return HttpResponse("There is no email profile at this link.")
    email_profile = email_profile[0]
    user = email_profile.user
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    if not email_profile.confirmed:
        login(request, user)
        link_age = email_profile.getAge()
        two_weeks_in_seconds = 60 * 60 * 24 * 14
        if link_age > two_weeks_in_seconds:
            email_profile.confirmation_link = getNewConfirmationLink()
            email_profile.created_when = datetime.datetime.now()
            email_profile.save()
            sendEmailAssociationConfirmation(email_profile)
            return HttpResponse("This confirmation link has expired. We sent you another confirmation email.")
        # if link not too old, we chillin
        email_profile.confirmed = True
        email_profile.save()
        return shortcuts.redirect("/initializing/")
    else:
        logError(
            "second time clicking on confirmation link? " + email_profile.email)
        return shortcuts.redirect("/login/")

def resendConfirmationLink(request):
    email_address = request.POST['email']
    try:
        email_profile = EmailProfile.objects.get(email=email_address)
    except ObjectDoesNotExist:
        logError("Attempt to reconfirm email address which was never registered: " + email_address)
        to_return = {"success":0}
        return json_response(to_return)
    email_profile.confirmation_link = getNewConfirmationLink()
    email_profile.created_when = datetime.datetime.now()
    email_profile.save()
    sendEmailAssociationConfirmation(email_profile)
    to_return = {"success":1}
    return json_response(to_return)

@ensure_csrf_cookie
def loginPage(request):
    if request.method == "GET":
        return render_to_response('login.html', locals(), context_instance=RequestContext(request))
    else:
        email = normalize_email(request.POST['email'])
        password = request.POST['password']
        error = ""
        try:
            email_profile = EmailProfile.objects.get(email=email)
        except ObjectDoesNotExist:
            error = "Oops, this email was not found. <br> Try <a href='/register/'>registering?</a>"
        except MultipleObjectsReturned:
            logError(
                "multiple email profiles for single email -- this is bad! " + str(email))
        else:
            if not email_profile.confirmed:
                error = "Oops, this email has not been confirmed. <br> <a class='reconfirm_button' href='/reconfirm/'> Resend? </a>"
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
            "error": error,
            "message": "blah"
        }
        return json_response(to_return)


def logoutPage(request):
    logout(request)
    return shortcuts.redirect("/login/")


@ensure_csrf_cookie
def registerPage(request):
    if request.method == "GET":
        return render_to_response('register.html', locals(), context_instance=RequestContext(request))
    else:
        email = normalize_email(request.POST['email'])
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        error = ""
        if not password1:
            error = "Oops, password can't be empty."
        elif not password1 == password2:
            error = "Oops, passwords must be the same."
        # check if email already exists
        already_profile = EmailProfile.objects.filter(
            email=email, confirmed=True)
        if already_profile:
            error = "This email is already associated with an account.<br> Try <a href='/login/'>logging in?</a>"
        already_user = User.objects.filter(username=email)
        if already_user:
            error = "This email is already associated with an account.<br> Try <a href='/login/'>logging in?</a>"
        if not error:
            user = User.objects.create_user(
                username=email, email=email, password=password1)
            send_mail(
                'ParselTongue Registration', email, 'settings@parseltongue.com',
                settings.HAPPY_EMAILS, fail_silently=True)  # nice email
        to_return = {
            "error": error,
            "message": "blah"
        }
        return json_response(to_return)

@csrf_exempt
def getPubKeys(request):

    requested_keys = json.loads(request.GET.get('requested_keys', []))
    requested_keys = map(normalize_email, requested_keys)
    res = {email: getPubKeysAssociatedWithEmail(email) for email in requested_keys}

    return json_response(res)


def getPubKeysAssociatedWithEmail(email):
    try:
        email_profile = EmailProfile.objects.get(email=email)
        user = email_profile.user
        return getUserPubKeys(user)
    except Exception:
        pass
    return []


def uploadPubKey(request):
    """
    Upload a pub key to your user account.
    """
    user = request.user
    pub_key_text = request.POST['pub_key']
    post_user = request.POST["username"]
    if user.username != post_user:
        logError("authenticated user is not who they think they are? " +
                 user.username + " " + post_user)
    prior_keys = PubKey.objects.filter(user=user)
    if prior_keys:
        pass
        # TODO: should send you an email saying a pub_key was uploaded to your
        # account, if not initial registration
    already = PubKey.objects.filter(user=user, pub_key_text=pub_key_text)
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
    post_user = request.POST["username"]
    if user.username != post_user:
        logError("authenticated user is not who they think they are? " +
                 user.username + " " + post_user)
    pri_key_text = request.POST['pri_key']
    already = PriKey.xobjects.get_or_none(user=user)
    if already:
        already.pri_key_text = pri_key_text
        already.save()
    else:
        pri_key = PriKey(user=user, pri_key_text=pri_key_text)
        pri_key.save()
    return HttpResponse("Success")


def getPriKey(request):
    user = request.user
    pri_key = PriKey.xobjects.get_or_none(user=user)
    if pri_key:
        to_return = {
            "success": 1,
            "pri_key": pri_key.pri_key_text
        }
    else:
        to_return = {
            "success": 0
        }
    return json_response(to_return)


@csrf_exempt
def ajaxError(request):
    user = request.user
    error = request.POST.get("error")
    email = ""
    if user and not user.is_anonymous():
        email = user.email
    error_message = "javascript error | user: " + email + " | " + error
    logError(error_message)
    return HttpResponse("error logged")
