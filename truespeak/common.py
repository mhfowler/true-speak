import uuid, random
from django.contrib.auth.models import User
from truespeak.models import EmailProfile
from django.core.mail import send_mail

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
    already = EmailProfile.objects.filter(email=email)
    if already:
        email_profile = already[0]
        if email_profile.user != user:
            print "Error: %s has already been assigned to another ParselTongue User. " % email
            return
        elif not email_profile.confirmed:
            email_profile.confirmed = True
            email_profile.save()
    else:
        email_profile = EmailProfile(user=user, email=email, confirmed=True)
        email_profile.save()


def sendEmailAssociationConfirmation(email_profile):
    confirmation_link = email_profile.getConfirmationLink()
    send_mail('ParselTongue Email Confirmation', confirmation_link, 'settings@parseltongue.com',
    [email_profile.email], fail_silently=False)


def getNewConfirmationLink():
    confirmation_link = None
    while not confirmation_link:
        confirmation_link = random.randint(0,10000000000)
        already = EmailProfile.objects.filter(confirmation_link=confirmation_link)
        if already:
            confirmation_link = None
    return confirmation_link
