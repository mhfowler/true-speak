from django.conf.urls import patterns, include, url
from truespeak.views import *
from django.conf import settings
from settings.common import PROJECT_PATH
import os

LOCAL_STATIC_FILES = os.path.join(PROJECT_PATH, 'truespeak/static/')

urlpatterns = patterns('',


                       (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': LOCAL_STATIC_FILES}),

                        # pages
                       ('^login/$', loginPage),
                       ('^logout/$', redirect, {'page':'/social/logout/'}),
                       (r'^home/$', home),
                       (r'^goodbye/$', goodbye),
                       (r'^about/$', about),
                       (r'^welcome/$', viewWrapper(welcome)),
                       (r'^settings/$', viewWrapper(settingsPage)),
                       (r'^confirm/(?P<link_number>\d+)/$', viewWrapper(confirmEmail)),

                       # ajax methods
                        (r'^get_pubkeys/$', viewWrapper(getPubKeys)),
                        (r'^upload_pubkey/$', viewWrapper(uploadPubKey)),
                        (r'^upload_prikey/$', viewWrapper(uploadPriKey)),

                       ('^/$', redirect),
                       ('^$', redirect),

                       # ('^channel/$', channel),
                       #
                       # (r'^connect_with_facebook/$', connect_with_facebook),
                       # (r'^facebook_callback/$', facebook_callback),
                       # (r'^done_token/$', done_token),
                       #
                       #
                       # (r'^upload_pubkey/$', upload_pubkey),
                       #
                       # (r'^friends/$', friends),
                       #
                       # (r'^set_encrypt/$', set_encrypt),

)


urlpatterns += patterns('',
                        # Here be other urls ...
                        url(r'^social/', include('socialregistration.urls',
                                                 namespace = 'socialregistration')))
