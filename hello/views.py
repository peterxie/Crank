from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .models import Greeting, User
import requests
import os
import logging
from django.conf import settings

fmt = getattr(settings, 'LOG_FORMAT', None)
lvl = getattr(settings, 'LOG_LEVEL', logging.INFO)

logging.basicConfig(format=fmt, level=lvl)
logging.info("Logging started on %s for %s" % (logging.root.name, logging.getLevelName(lvl)))
# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

def showSignUp(request):
    return render(request, 'signup.html')
@csrf_exempt
def signUp(request):
    if request.method == 'GET':
        return
    logging.info(str(request.POST))
    user = User(name = request.POST.get('inputName'), 
                userName = request.POST.get('inputEmail'), 
                password = request.POST.get('inputPassword'))
    logging.info("user: %s, name: %s, pass: %s" % (user.name, user.userName, user.password))
    user.save()
    users = User.objects.all()
    return redirect('users')

@csrf_exempt
def delete(request):
	if request.method == 'GET':
		return
	User.objects.all().delete();
	logging.info(str(request.POST))
	return redirect('users')

def users(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

