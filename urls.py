from django.conf.urls import patterns, include, url
from truespeak.views import *
from django.conf import settings

urlpatterns = patterns('',


                       (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

                       ('^login/$', loginPage),
                       (r'^home/$', home),
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
