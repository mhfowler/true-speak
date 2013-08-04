from truespeak.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'd16lqneqfq7hoo',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'kgxrugdylnkwgc',
        'PASSWORD': 'Mfe7ufY3bYXSeXtlRc9IIhL8s2',
        'HOST': 'ec2-107-20-224-218.compute-1.amazonaws.com',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '5432',                      # Set to empty string for default.
    }
}