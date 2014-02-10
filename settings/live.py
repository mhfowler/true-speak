from settings.common import *

DATABASES = {
    'default': SECRETS_DICT['DATABASES']['LIVE']
}

STATIC_URL = "https://s3.amazonaws.com/parseltongue/"

# https settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

MIDDLEWARE_CLASSES_LIST.insert(0,'sslify.middleware.SSLifyMiddleware')
MIDDLEWARE_CLASSES = tuple(MIDDLEWARE_CLASSES_LIST)