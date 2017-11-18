from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings

from django.core.mail import send_mail

from .forms import *
from .tokens import account_activation_token
from .models import Rating_id, Course_Faculty_Table, Rating_Average
from .filters import *
import requests
import os
import logging
from operator import add

fmt = getattr(settings, 'LOG_FORMAT', None)
lvl = getattr(settings, 'LOG_LEVEL', logging.INFO)

logging.basicConfig(format=fmt, level=lvl)
logging.info("Logging started on %s for %s" % (logging.root.name, logging.getLevelName(lvl)))

def index(request):
    return render(request, 'index.html')

def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'account_activation_invalid.html')

@login_required(login_url='/login')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='/login')
def rank(request):
    if request.method == 'POST':
        form = RankForm(request.POST)
        if form.is_valid():
            try:
                course_pair = form.cleaned_data.get("course_faculty_pair")
                user = User.objects.get(username=request.user)

                rating = Rating_id(uni=user,
                                   course=course_pair,  
                                   usefulness=form.cleaned_data.get("usefulness"),
                                   lecture_quality=form.cleaned_data.get("lecture_quality"),
                                   overall_quality=form.cleaned_data.get("overall_quality"),
                                   oral_written_tests_helpful=form.cleaned_data.get("oral_written_tests_helpful"),
                                   learned_much_info=form.cleaned_data.get("learned_much_info"))
                rating.save()
            except Exception as e:
                logging.error(e)
                status_code = 400
                message = "Ranking is not valid!"
                explanation = "Error - you have already submitted a ranking for this class/faculty pairing"
                return JsonResponse({'message':message, 'explanation':explanation}, status = status_code)

            return redirect('home')
    else:
        form = RankForm()
    return render(request, 'rank.html', {'form':form})

def display(request):
    ratings = Rating_id.objects.all()
    course_faculty = Course_Faculty_Table.objects.all()

    rating_dict = {}
    for rating in ratings:
        n = Rating_id.objects.filter(course=rating.course).count()
        if rating.course not in rating_dict:
            rating_dict[rating.course] = [rating.usefulness/n, rating.lecture_quality/n, rating.overall_quality/n, rating.oral_written_tests_helpful/n, rating.learned_much_info/n]
        else:
            rating_dict[rating.course] = list(map(add,rating_dict[rating.course],[rating.usefulness/n, rating.lecture_quality/n, rating.overall_quality/n, rating.oral_written_tests_helpful/n, rating.learned_much_info/n]))
    
    for key,value in rating_dict.items():
        rating_average = Rating_Average(course=key,
                                        usefulness=value[0],
                                        lecture_quality=value[1],
                                        overall_quality=value[2],
                                        oral_written_tests_helpful=value[3],
                                        learned_much_info=value[4])
        rating_average.save()
    order_by = request.GET.get('order_by', 'usefulness')
    rating_average = Rating_Average.objects.order_by("-"+order_by)
    
    return render(request, 'display.html', {'rating_average': rating_average})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.username + "@columbia.edu"
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Crank Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required(login_url='/login')
def manage_account(request):
    user = User.objects.get(username=request.user)
    return render(request, 'account_management.html', {'user': user})

@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            try:
                old_password, new_password = form.clean_password()
                form.save(request.user, old_password, new_password)
                return redirect('/manage_account')
            except Exception as e:
                logging.error(e)
                if e.code == 'incorrect_password':
                  form.add_error('old_password', e.message)
                else:
                  form.add_error('new_password1', e.message)
    else:
        form = ChangePasswordForm()
    return render(request, 'change_password.html', {'form':form})
