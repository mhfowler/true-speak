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

#-----------------------------------------------------------------------------------------------------------------------
# UserProfile
#-----------------------------------------------------------------------------------------------------------------------
# class UserProfile(XModel):
#     user = models.ForeignKey(User, unique=True)
#     pubkeys = models.TextField(default = "[]")
#     plugin_token = models.CharField(max_length=400)
#     will_encrypt = models.BooleanField(default = True)
#     # info from fb
#     fb_id = models.CharField(max_length=400, null=True)
#     fb_handle = models.CharField(max_length=400)
#     friends_ids = models.TextField()    # json of list of fb_ids of friends
#     first_name = models.CharField(max_length=400,null=True)
#     last_name = models.CharField(max_length=400,null=True)
#
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#
# post_save.connect(create_user_profile, sender=User)

