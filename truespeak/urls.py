from django.conf.urls import patterns, include, url
from truespeak.views import viewWrapper, login_page, home, redirect, register

urlpatterns = patterns('',

   (r'^login/$', login_page),
   (r'^register/$', register),
   (r'^home/$', viewWrapper(home)),
   (r'.*$',  redirect, {'page':"/home/"}),

)
