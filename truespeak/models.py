from django.db import models
from django.contrib.auth.models import User

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
class UserProfile(XModel):
    user = models.ForeignKey(User, unique=True)

