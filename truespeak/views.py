from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django import shortcuts
from truespeak.models import *


def redirect(request, page='/home'):
    return shortcuts.redirect(page)


def login_page(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse("logged in")
    else:
        return HttpResponse("invalid")


def register(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    if username and password:
        if User.objects.filter(username=username):
            return HttpResponse("already registered")
        user = User.objects.create_user(username=username, email=username, password=password)
        user.save()
        user_profile = UserProfile()
        user_profile.user = user
        user_profile.save()
        return HttpResponse("registered")


def viewWrapper(view):
    def new_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponse("You need to be logged in doe")
        else:
            return view(request,*args,**kwargs)
    return new_view


def home(request):
    return HttpResponse("hello world")