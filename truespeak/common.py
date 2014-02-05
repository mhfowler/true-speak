from truespeak.models import EmailProfile, logger
from django.core.mail import send_mail
from django.conf import settings

from validate_email import validate_email

import os
import binascii

INVALID_EMAIL = "Email is not valid!"


def send_email_confirmation(email_profile):
    confirmation_link = "https://getparseltongue.com" + \
        email_profile.getConfirmationLink()
    message = "Dear " + email_profile.email + ",\n\n" \
        "To confirm your email address with ParselTongue please click this link: \n\n"  + confirmation_link + "\n\n" \
        "Confirming your email will allow other ParselTongue users to encrpyt their emails to you using your public key. " \
        "The only copy of the private key that matches your public key exists on your laptop. \n\n" \
        "Truly,\n" \
        "Max, Josh and Stephanie\n" \
        "https://getparseltongue.com/faq/"
    send_mail(
        'ParselTongue Email Confirmation', message, 'settings@parseltongue.com',
        [email_profile.email], fail_silently=False)


def send_prikey_warning(user):
    email = user.email
    disable_link = "http://getparseltongue.com/disable/" + email + "/"
    message = "Dear " + email + ",\n\n" \
        "Someone (hopefully you) just logged in to ParselTongue as you on a new computer. If this was not you "  \
        "please click the link below and we will disable your account: \n\n"  + disable_link + "\n\n" \
        "If you click the disable link you will receive a notification email once your account has been disabled " \
        "and will then be able to reregister if you choose to. \n\n" \
        "Truly,\n" \
        "Max, Josh and Stephanie\n" \
        "https://getparseltongue.com/faq/"
    send_mail(
        'ParselTongue Login Notification', message, 'settings@parseltongue.com',
        [email], fail_silently=False)


def get_new_confirm_link():
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


def log_error(message):
    send_mail('ParselTongue Javascript Error', message,
              'getparseltongue@gmail.com', settings.ERROR_EMAILS, fail_silently=True)
    logger.error(message)


# returns True if no error, false otherwise (tuple)
def create_email_profile(new_email, user):
    already = EmailProfile.objects.filter(email=new_email)

    if not validate_email(new_email):
        return False, INVALID_EMAIL

    if already:
        email_profile = already[0]
        alternate_email = already.filter(user=user)
        if alternate_email:
            return False, "This email address is already associated with you, silly!"
        elif email_profile.confirmed:
            return False, "This email address is already associated with a ParselTongue user."
        else:
            email_profile.user = user
            email_profile.confirmation_link = get_new_confirm_link()
            email_profile.save()
            send_email_confirmation(email_profile)
            return True, "A confirmation email has been sent to your email address."
    else:
        email_profile = EmailProfile(
            email=new_email, user=user, confirmed=False)
        email_profile.confirmation_link = get_new_confirm_link()
        email_profile.save()
        send_email_confirmation(email_profile)
        return True, "A confirmation email has been sent to your email address."


def normalize_email(email):
    return email.lower()


def template_values(request, page_title='', navbar='', **kwargs):
    template_values = {
        'page_title': page_title,
        navbar: 'active',
    }

    return dict(template_values.items() + kwargs.items())
