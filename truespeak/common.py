from django.contrib.auth.models import User
from truespeak.models import EmailProfile, logger
from django.core.mail import send_mail
from django.conf import settings# import settings.ERROR_EMAILS

import uuid
import os
import binascii
import random


def sendTestMessage():
    message = "<div> You should see this. </div><div style='display:none;'>You should not see this</div>"
    send_mail('Test Email', message, 'parseltongueextension@gmail.com',
              ['max_fowler@brown.edu'], fail_silently=True)


def generateRandomUsername():
    username = None
    while not username:
        username = uuid.uuid4().hex[:10]
        already = User.objects.filter(username=username)
        if already:
            username = None
    return username


def addAssociatedEmailProfile(user, email):
    """
     force add an email address to be associated with a user
    """
    already = EmailProfile.objects.filter(email=email, confirmed=True)
    if already:
        email_profile = already[0]
        if email_profile.user != user:
            logError(
                "Error: %s has already been assigned to another ParselTongue User. " % email)
            return
    else:
        email_profile = EmailProfile(user=user, email=email)
        email_profile.save()


def sendEmailAssociationConfirmation(email_profile):
    confirmation_link = "http://www.parseltongueextension.com" + \
        email_profile.getConfirmationLink()
    message = "Dear " + email_profile.email + ",\n\n" \
        "To confirm your email address with ParselTongue please click this link: \n\n"  + confirmation_link + "\n\n" \
        "Confirming your email will allow other ParselTongue users to encrpyt their emails to you using your public key. " \
        "The only copy of the private key that matches your public key exists on your laptop. \n\n" \
        "Truly,\n" \
        "Max, Josh and Stephanie\n" \
        "http://www.parseltongueextension.com/about/"
    send_mail(
        'ParselTongue Email Confirmation', message, 'settings@parseltongue.com',
        [email_profile.email], fail_silently=False)


def sendPriKeyDownloadWarning(user):
    email = user.email
    disable_link = "http://www.parseltongueextension.com/disable/" + email + "/"
    message = "Dear " + email + ",\n\n" \
        "Someone (hopefully you) just logged in to ParselTongue as you on a new computer. If this was not you "  \
        "please click the link below and we will disable your account: \n\n"  + disable_link + "\n\n" \
        "If you click the disable link you will receive a notification email once your account has been disabled " \
        "and will then be able to reregister with a new uncompromised password if you choose to. \n\n" \
        "Truly,\n" \
        "Max, Josh and Stephanie\n" \
        "http://www.parseltongueextension.com/about/"
    send_mail(
        'ParselTongue Login Notification', message, 'settings@parseltongue.com',
        [email], fail_silently=False)


def getNewConfirmationLink():
    confirmation_link = None
    while not confirmation_link:
        confirmation_link = ""
        for i in range(0, 3):
            confirmation_link += binascii.b2a_hex(os.urandom(15))
        print confirmation_link
        already = EmailProfile.objects.filter(
            confirmation_link=confirmation_link)
        if already:
            confirmation_link = None
    return confirmation_link


def logError(message):
    send_mail('ParselTongue Javascript Error', message,
              'parseltongueextension@gmail.com', settings.ERROR_EMAILS, fail_silently=True)
    logger.error(message)


# returns True if no error, false otherwise (tuple)
def createEmailProfile(new_email, user):
    already = EmailProfile.objects.filter(email=new_email)
    if already:
        email_profile = already[0]
        alternate_email = already.filter(user=user)
        if alternate_email:
            return False, "This email address is already associated with you, silly!"
        elif email_profile.confirmed:
            return False, "This email address is already associated with a ParselTongue user."
        else:
            email_profile.user = user
            email_profile.confirmation_link = getNewConfirmationLink()
            email_profile.save()
            sendEmailAssociationConfirmation(email_profile)
            return True, "A confirmation email has been sent to your email address."
    else:
        email_profile = EmailProfile(
            email=new_email, user=user, confirmed=False)
        email_profile.confirmation_link = getNewConfirmationLink()
        email_profile.save()
        sendEmailAssociationConfirmation(email_profile)
        return True, "A confirmation email has been sent to your email address."


def normalize_email(email):
    return email.lower()

def _template_values(request, page_title='', navbar='', **kwargs):
    template_values = {
        'page_title' : page_title,
        navbar : 'active',
    }

    return dict(template_values.items() + kwargs.items())
