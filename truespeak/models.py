from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save

import logging
import datetime

# Get an instance of a logger
logger = logging.getLogger(__name__)


#-------------------------------------------------------------------------
# Useful manager for all models.
#-------------------------------------------------------------------------
class XManager(models.Manager):

    """Adds get_or_none method to objects
    """

    def get_or_none(self, **kwargs):
        res = self.filter(**kwargs)
        if res:
            return res[0]
        return res

#-------------------------------------------------------------------------
# All models inherit from this
#-------------------------------------------------------------------------


class XModel(models.Model):
    xobjects = XManager()
    objects = models.Manager()

    class Meta:
        abstract = True

# ------------------------------------------------------------------------
# EmailProfile. associate as many email addresses
# as you want with parseltongue user
# ------------------------------------------------------------------------


class EmailProfile(XModel):
    user = models.ForeignKey(User)
    email = models.EmailField(unique=True)
    confirmed = models.BooleanField(default=False)
    created_when = models.DateTimeField(auto_now_add=True, blank=True)
    confirmation_link = models.CharField(max_length=100)

    def getConfirmationLink(self):
        return "/confirm/" + str(self.confirmation_link) + "/"

    def getAge(self):
        now = datetime.datetime.now()
        age = now - self.created_when.replace(tzinfo=None)
        return age.total_seconds()


def getAssociatedEmailAddresses(user):
    emails = EmailProfile.objects.filter(user=user)
    return [(email.email, email.confirmed) for email in emails]


def removeEmailAddress(email, user):
    '''
    removes an (alternate) email address for a user
    returns False if the email is user's primary email
    '''
    if email == user.email:
        return False
    # TODO: for now, don't allow deletion of email if it's confirmed, not
    # sure how to handle yet if user really does want to delete
    email = EmailProfile.xobjects.get(email=email, user=user)
    if email and email.confirmed:
        return False

    email.delete()
    return True

#-------------------------------------------------------------------------
# Pubkey
#-------------------------------------------------------------------------


class PubKey(XModel):
    user = models.ForeignKey(User)
    pub_key_text = models.CharField(max_length=200)


def getUserPubKeys(user):
    keys = PubKey.objects.filter(user=user)
    return [key.pub_key_text for key in keys]

#-------------------------------------------------------------------------
# Prikey... should be stored encrypted (via a password only the user knows)
#-------------------------------------------------------------------------


class PriKey(XModel):
    user = models.OneToOneField(User)
    pri_key_text = models.TextField()


def getUserPriKey(user):
    try:
        pri_key = PriKey.objects.get(user=user)
        return pri_key.pri_key_text
    except ObjectDoesNotExist:
        return None

#-------------------------------------------------------------------------
# Post save function for auth user.
#-------------------------------------------------------------------------


def authUserPostSave(sender, **kwargs):
    user = kwargs['instance']
    created = kwargs['created']
    if created:
        from truespeak.common import createEmailProfile
        createEmailProfile(user.email, user)

post_save.connect(authUserPostSave,
                  sender=User, dispatch_uid="auth_user_post_save")
