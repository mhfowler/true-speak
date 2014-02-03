from settings.common import *

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "parseltongue",
        "USER": "root",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": ""
    }
}


HAPPY_EMAILS = [
    "maximusfowler@gmail.com",
]

ERROR_EMAILS = HAPPY_EMAILS