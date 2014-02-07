from django.conf.urls import patterns, include
from truespeak.views import *
from settings.common import PROJECT_PATH
import os

LOCAL_STATIC_FILES = os.path.join(PROJECT_PATH, 'truespeak/static/')

urlpatterns = patterns('',
                      (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
                       'document_root': LOCAL_STATIC_FILES
                       }),
                       (r'^robots\.txt$', lambda r: HttpResponse(
                           "User-agent: *\nDisallow: /", mimetype="text/plain")),

                       # pages
                       (r'^sendgrid/$', lambda r: HttpResponse(
                           "sendgrid", mimetype="text/plain")),
                       (r'^register/$', register),
                       (r'^login/$', login_),
                       (r'^logout/$', logout_),
                       (r'^home/$', home),
                       (r'^faq/$', faq),
                       (r'^team/$', team),
                       (r'^tutorial/$', tutorial),
                       (r'^welcome/(?P<email_address>\S*)/$', welcome),
                       (r'^settings/$', settings_),
                       (r'^initializing/$', initializing),
                       (r'^disable/(?P<email_address>\S*)/$',
                        disable_account),
                       (r'^confirm/(?P<link_number>\S*)/$', confirm_email),
                       (r'^reconfirm/$', reconfirm),

                       # ajax methods
                      (r'^get_pubkeys/$', get_pubkeys),
                      (r'^get_prikey/$', get_prikey),
                      (r'^upload_pubkey/$', upload_pubkey),
                      (r'^upload_prikey/$', upload_prikey),
                      (r'^error/$', error),
                      (r'^extension_sync/$', extension_sync),
                      (r'^extension_ack/$', extension_ack),
                      (r'^ext/', include("extension.urls")),

                      (r'^/$', home),
                      (r'^$', home),

                       )
