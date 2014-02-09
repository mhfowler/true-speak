# Django settings for truespeak project.
import os
import json

PROJECT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

LOCAL = os.environ.get("LOCAL")
DEBUG = False
TEMPLATE_DEBUG = DEBUG

LOGIN_URL = "/login"

SECRETS_PATH = os.path.join(PROJECT_PATH, "secret.json")

if LOCAL:  # export LOCAL=1
    DEBUG = True
    SECRETS_DICT = json.loads(open(SECRETS_PATH, "r").read())
    DOMAIN = "local.parseltongueextension.com"
else:
    SECRETS_ENV = os.environ.get("SECRETS")
    SECRETS_DICT = json.loads(SECRETS_ENV)
    DOMAIN = "getparseltongue.com"

ADMINS = (
    ("Max Fowler", "maximusfowler@gmail.com"),
    ("Josh Blum", "joshblum@mit.edu"),
    ("Stephanie Wang", "swang93@mit.edu")
)

HAPPY_EMAILS = [
    "maximusfowler@gmail.com",
    "joshblum@mit.edu",
    "swang93@mit.edu"
]

ERROR_EMAILS = HAPPY_EMAILS

MANAGERS = ADMINS

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': '',
        # Or path to database file if using sqlite3.
        'NAME': '',
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        # Empty for localhost through domain sockets or '127.0.0.1' for
        # localhost through TCP.
        'HOST': '',
        'PORT': '',                      # Set to empty string for default.
    }
}


# SENDGRID
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'getparseltongue'
EMAIL_HOST_PASSWORD = SECRETS_DICT['EMAIL_PASSWORD']
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# AUTH_PROFILE_MODULE = 'truespeak.UserProfile'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

# settings for django-compressor
COMPRESS_ENABLED = not DEBUG
COMPRESS_CSS_FILTERS = (
    'compressor.filters.template.TemplateFilter',
)

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    "*",
]
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), "media")

MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',

    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '&66fite8%&_#6v-_j+eg_d2@^^8+r3gcvufp-aee0%g$hd85@x'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    # 'sslify.middleware.SSLifyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.csrf',
)

# cross domain sharing
XS_SHARING_ALLOWED_HEADERS = [
    "x-csrftoken",
]

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), "templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',

    # third party
    'compressor',
    'south',
    'storages',

    'truespeak',
    'extension'

    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(PROJECT_PATH, 'logs/pt.log'),
            'maxBytes': '16777216',  # 16megabytes
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        '': {
            'handlers': ['mail_admins', 'log_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

# s3

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = SECRETS_DICT["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = SECRETS_DICT["AWS_SECRET_ACCESS_KEY"]
AWS_STORAGE_BUCKET_NAME = "parseltongue"
from S3 import CallingFormat
AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN

STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# https settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('X-FORWARDED-PROTO', 'https')
