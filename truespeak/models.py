from django.db import models
from django.contrib.auth.models import User
import random
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models.signals import post_save


#-----------------------------------------------------------------------------------------------------------------------
# Useful manager for all models.
#-----------------------------------------------------------------------------------------------------------------------
class XManager(models.Manager):
    """Adds get_or_none method to objects
    """
    def get_or_none(self, **kwargs):
        to_return = self.filter(**kwargs)
        if to_return:
            return to_return[0]
        else:
            return to_return

#-----------------------------------------------------------------------------------------------------------------------
# All models inherit from this
#-----------------------------------------------------------------------------------------------------------------------
class XModel(models.Model):
    lg = XManager()
    objects = models.Manager()
    class Meta:
        abstract = True

# -----------------------------------------------------------------------------------------------------------------------
# EmailProfile. associate as many email addresses as you want with parseltongue user
# -----------------------------------------------------------------------------------------------------------------------
class EmailProfile(XModel):
    user = models.ForeignKey(User)
    email = models.EmailField(unique=True)
    confirmed = models.BooleanField(default=False)
    created_when = models.DateTimeField(auto_now_add=True, blank=True)
    confirmation_link = models.CharField(max_length=100)

    def getConfirmationLink(self):
        return "/confirm/" + str(self.confirmation_link) + "/"

def getAssociatedEmailAddresses(user, confirmed=True):
    emails = EmailProfile.objects.filter(user=user)
    if confirmed:
        emails = emails.filter(confirmed=True)
    to_return = []
    for x in emails:
        to_return.append(x.email)
    return to_return

# -----------------------------------------------------------------------------------------------------------------------
# Pubkey
# -----------------------------------------------------------------------------------------------------------------------
class PubKey(XModel):
    user = models.ForeignKey(User)
    pub_key_text = models.CharField(max_length=200)

def getUserPubKeys(user):
    pub_keys = PubKey.objects.filter(user=user)
    to_return = []
    for x in pub_keys:
        to_return.append(x.pub_key_text)
    return to_return

# -----------------------------------------------------------------------------------------------------------------------
# Prikey... should be stored encrypted (via a password only the user knows)
# -----------------------------------------------------------------------------------------------------------------------
class PriKey(XModel):
    user = models.OneToOneField(User)
    pri_key_text = models.CharField(max_length=200)

def getUserPriKey(user):
    try:
        pri_key = PriKey.objects.get(user=user)
        return pri_key.pri_key_text
    except ObjectDoesNotExist as e:
        return None

#-----------------------------------------------------------------------------------------------------------------------
# Post save function for auth user.
#-----------------------------------------------------------------------------------------------------------------------
def authUserPostSave(sender, **kwargs):
    user = kwargs['instance']
    if user.email:
        from truespeak.common import addAssociatedEmailProfile
        addAssociatedEmailProfile(user, user.email)

post_save.connect(authUserPostSave, sender=User, dispatch_uid="auth_user_post_save")