from django.contrib.auth.models import User
from settings.common import LOCAL

if not LOCAL:
    print "wtf are you doing? do not delete all users on prod."
else:
    for x in User.objects.all():
        x.delete()

