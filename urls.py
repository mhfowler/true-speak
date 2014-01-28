from django.conf.urls import patterns, include, url
from truespeak.views import *
from django.conf import settings
from settings.common import PROJECT_PATH
import os

LOCAL_STATIC_FILES = os.path.join(PROJECT_PATH, 'truespeak/static/')

urlpatterns = patterns('',
                       (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
                        'document_root': LOCAL_STATIC_FILES}),

                       # pages
                       ('^register/$', registerPage),
                       ('^login/$', loginPage),
                       ('^logout/$', viewWrapper(logoutPage)),
                       (r'^home/$', home),
                       (r'^goodbye/$', goodbye),
                       (r'^about/$', about),
                       (r'^tutorial/$', tutorial),
                       (r'^contact/$', contact),
                       (r'^welcome/(?P<email_address>\S*)/$', welcome),
                       (r'^settings/$', viewWrapper(settingsPage)),
                       (r'^initializing/$', viewWrapper(initializingPage)),
                       (r'^disable/(?P<email_address>\S*)/$', viewWrapper(disableAccount)),
                       (r'^confirm/(?P<link_number>\S*)/$', confirmEmail),
                       (r'^reconfirm/$', resendConfirmationLink),

                       # ajax methods
                      (r'^get_pubkeys/$', getPubKeys),
                      (r'^get_prikey/$', viewWrapper(getPriKey)),
                      (r'^upload_pubkey/$', viewWrapper(uploadPubKey)),
                      (r'^upload_prikey/$', viewWrapper(uploadPriKey)),
                      (r'^error/$', ajaxError),

                       ('^/$', redirect),
                       ('^$', redirect),

                       )
