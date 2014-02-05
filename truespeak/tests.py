from truespeak.models import *

def userStats():
    users = User.objects.all()
    stats = {
        "users":[],
        "yespub_nopri":[],
        "nopub_yespri":[],
        "yespub_yespri":[],
        "nopub_nopri":[],
        "multi_pri": [],
        "multi_pub": [],
        "confirmed":[],
        "confirmed_nopub":[],
        "unconfirmed":[],
        "unconfirmed_yespub":[],
    }
    user_counts = {}
    for u in users:
        username = u.username
        user_counts[username] = result = getUserCounts(u)
        num_email_profiles = result["num_email_profiles"]
        num_confirmed_email_profiles = result["num_confirmed_email_profiles"]
        num_pub_keys = result["num_pub_keys"]
        num_pri_keys = result["num_pri_keys"]
        # do something comparing numbers and adding to abnormalities
        stats["users"].append(username)
        if num_pub_keys and not num_pub_keys:
            stats["yespub_nopri"].append(username)
        if not num_pub_keys and num_pri_keys:
            stats["nopub_yespri"].append(username)
        if num_pub_keys and num_pri_keys:
            stats["yespub_yespri"].append(username)
        if not num_pub_keys and not num_pri_keys:
            stats["nopub_nopri"].append(username)
        if num_pri_keys > 1:
            stats["multi_pri"].append(username)
        if num_pub_keys > 1:
            stats["multi_pub"].append(username)
        if num_confirmed_email_profiles:
            stats["confirmed"].append(username)
        if num_confirmed_email_profiles and not num_pub_keys:
            stats["confirmed_nopub"].append(username)
        if not num_confirmed_email_profiles:
            stats["unconfirmed"].append(username)
        if not num_confirmed_email_profiles and num_pub_keys:
            stats["unconfirmed_yespub"].append(username)

    for k,v in stats.items():
        print k + ": " + str(len(v))

    # warnings
    if len(stats["yespub_nopri"]): print "+WW+: yespub_nopri"
    if len(stats["nopub_yespri"]): print "+WW+: nopub_yespri"
    if len(stats["multi_pri"]): print "+WW+: multi_pri"
    if len(stats["multi_pub"]): print "+WW+: multi_pub"
    if len(stats["confirmed_nopub"]): print "+WW+: confirmed_nopub"
    if len(stats["unconfirmed_yespub"]): print "+WW+: confirmed_yespub"


def getUserCounts(u):
    email_profiles = EmailProfile.objects.filter(user=u)
    num_email_profiles = email_profiles.count()
    num_pub_keys = PubKey.objects.filter(user=u).count()
    num_pri_keys = PriKey.objects.filter(user=u).count()
    is_user_confirmed = False
    num_confirmed_email_profiles = 0
    for x in email_profiles:
        if x.confirmed:
            is_user_confirmed = True
            num_confirmed_email_profiles += 1
    return {
        "num_email_profiles":num_email_profiles,
        "num_confirmed_email_profiles":num_confirmed_email_profiles,
        "num_pri_keys":num_pri_keys,
        "num_pub_keys":num_pub_keys
    }

if __name__ == "__main__":
    userStats()

