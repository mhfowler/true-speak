from django.conf.urls import patterns, url

urlpatterns = patterns('extension.views',
                       url(r'^login$', 'login'),
                       )
