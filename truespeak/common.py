from django.contrib.auth.models import User
from truespeak.models import EmailProfile, logger
from django.core.mail import send_mail

import uuid
import random


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


def getNewConfirmationLink():
    confirmation_link = None
    while not confirmation_link:
        confirmation_link = random.randint(0, 10000000000)
        already = EmailProfile.objects.filter(
            confirmation_link=confirmation_link)
        if already:
            confirmation_link = None
    return confirmation_link


def logError(message):
    logger.error(message)


# returns True if no error, false otherwise (tuple)
def createEmailProfile(new_email, user):
    already = EmailProfile.objects.filter(email=new_email)
    if already:
        email_profile = already[0]
        if email_profile.confirmed:
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
