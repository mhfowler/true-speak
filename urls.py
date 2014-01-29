from django.conf.urls import patterns, include, url
from truespeak.views import *
from django.conf import settings
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

                       (r'^register/$', registerPage),
                       (r'^login/$', loginPage),
                       (r'^logout/$', view_wrapper(logoutPage)),
                       (r'^home/$', home),
                       (r'^faq/$', faq),
                       (r'^team/$', team),
                       (r'^tutorial/$', tutorial),
                       (r'^welcome/(?P<email_address>\S*)/$', welcome),
                       (r'^settings/$', view_wrapper(settingsPage)),
                       (r'^initializing/$', view_wrapper(initializingPage)),
                       (r'^disable/(?P<email_address>\S*)/$',
                        view_wrapper(disableAccount)),
                       (r'^confirm/(?P<link_number>\S*)/$', confirmEmail),
                       (r'^reconfirm/$', resendConfirmationLink),

                       # ajax methods
                      (r'^get_pubkeys/$', getPubKeys),
                      (r'^get_prikey/$', view_wrapper(getPriKey)),
                      (r'^upload_pubkey/$', view_wrapper(uploadPubKey)),
                      (r'^upload_prikey/$', view_wrapper(uploadPriKey)),
                      (r'^error/$', ajaxError),

                      ('^/$', redirect),
                      ('^$', redirect),

                       )
