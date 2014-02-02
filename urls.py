from django.conf.urls import patterns
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
                       (r'^logout/$', view_wrapper(logout_)),
                       (r'^home/$', home),
                       (r'^faq/$', faq),
                       (r'^team/$', team),
                       (r'^tutorial/$', tutorial),
                       (r'^welcome/(?P<email_address>\S*)/$', welcome),
                       (r'^settings/$', view_wrapper(settings_)),
                       (r'^initializing/$', view_wrapper(initializing)),
                       (r'^disable/(?P<email_address>\S*)/$',
                        view_wrapper(disable_account)),
                       (r'^confirm/(?P<link_number>\S*)/$', confirm_email),
                       (r'^reconfirm/$', reconfirm),
                       (r'^test/$', testPage),

                       # ajax methods
                      (r'^get_pubkeys/$', get_pubkeys),
                      (r'^get_prikey/$', view_wrapper(get_prikey)),
                      (r'^upload_pubkey/$', view_wrapper(upload_pubkey)),
                      (r'^upload_prikey/$', view_wrapper(upload_prikey)),
                      (r'^error/$', error),

                      (r'^/$', home),
                      (r'^$', home),

                       )
