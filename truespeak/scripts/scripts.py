from truespeak.models import *

def deleteUser(email):
    print "deleting: " + email
    user = User.objects.get(username=email)
    pub_keys = PubKey.objects.filter(user=user)
    pri_keys = PriKey.objects.filter(user=user)
    email_profiles = EmailProfile.objects.filter(user=user)
    pub_keys.delete()
    pri_keys.delete()
    email_profiles.delete()
    user.delete()


