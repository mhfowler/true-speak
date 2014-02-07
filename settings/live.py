from settings.common import *

DATABASES = {
    'default': SECRETS_DICT['DATABASES']['LIVE']
}

STATIC_URL = "https://s3.amazonaws.com/parseltongue/"