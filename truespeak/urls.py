from django.conf.urls import patterns, include, url
from truespeak.views import *

import settings

urlpatterns = patterns('',


	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

	('^channel/$', channel),

	(r'^connect_with_facebook/$', connect_with_facebook),
   	(r'^facebook_callback/$', facebook_callback),

   	(r'^upload_pubkey/$', upload_pubkey),

   	(r'^friends/$', friends),

   	
)
