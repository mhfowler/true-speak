from django.db import models
from django.contrib.auth.models import User

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

class Facebook_User(XModel):
    
    fb_id = models.CharField(max_length=400)
    handle = models.CharField(max_length=400)
    first_name = models.CharField(max_length=400,null=True)
    last_name = models.CharField(max_length=400,null=True)

#-----------------------------------------------------------------------------------------------------------------------
# UserProfile
#-----------------------------------------------------------------------------------------------------------------------
class UserProfile(XModel):
    user = models.ForeignKey(User, unique=True)
    facebook_user = models.ForeignKey(Facebook_User, unique=True, null = True, blank = True)
    friends = models.ManyToManyField(Facebook_User,null=True, related_name='+')

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

