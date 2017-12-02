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
                                   course_faculty=course_pair,  
                                   usefulness=form.cleaned_data.get("usefulness"),
                                   lecture_quality=form.cleaned_data.get("lecture_quality"),
                                   overall_quality=form.cleaned_data.get("overall_quality"),
                                   oral_written_tests_helpful=form.cleaned_data.get("oral_written_tests_helpful"),
                                   learned_much_info=form.cleaned_data.get("learned_much_info"))
                rating.save()

                rating_avg = Rating_Average.objects.filter(course_faculty=course_pair).first()
                if rating_avg is not None:
                    count = rating_avg.rating_count
                    print('usefulness')
                    rating_avg.usefulness = (rating_avg.usefulness*count + float(rating.usefulness))/(count+1)
                    print('lecture_quality')
                    rating_avg.lecture_quality = (rating_avg.lecture_quality*count + float(rating.lecture_quality))/(count+1)
                    rating_avg.overall_quality = (rating_avg.overall_quality*count + float(rating.overall_quality))/(count+1)
                    rating_avg.oral_written_tests_helpful = (rating_avg.oral_written_tests_helpful*count + float(rating.oral_written_tests_helpful))/(count+1)
                    rating_avg.learned_much_info = (rating_avg.learned_much_info*count + float(rating.learned_much_info))/(count+1)
                    rating_avg.rating_count = count+1
                else:
                    rating_avg = Rating_Average(course_faculty=course_pair,
                                                usefulness=rating.usefulness,
                                                lecture_quality=rating.lecture_quality,
                                                overall_quality=rating.overall_quality,
                                                oral_written_tests_helpful=rating.oral_written_tests_helpful,
                                                learned_much_info=rating.learned_much_info,
                                                rating_count=1)


                rating_avg.save()
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
def show_history(request):
    user = User.objects.get(username=request.user)

    order_by = request.GET.get('order_by', 'course_faculty')
    history = Rating_id.objects.filter(uni=user.id).order_by("-"+order_by)

    return render(request, 'history.html', {'history': history})

@login_required(login_url='/login')
def delete_rank(request,delete_id=None):
    user = User.objects.get(username=request.user)
    rank_to_delete = Rating_id.objects.filter(uni=user.id,id=delete_id).first()
    course_to_update = rank_to_delete.course_faculty
    rating_avg = Rating_Average.objects.filter(course = course_to_update).first()

    u = rating_avg.usefulness
    lq = rating_avg.lecture_quality
    oq = rating_avg.overall_quality
    owth = rating_avg.oral_written_tests_helpful
    lmi = rating_avg.learned_much_info
    rc = rating_avg.rating_count

    if rc == 1:
    	rating_average.delete()
    else:
        rating_avg.usefulness = (u*rc - rank_to_delete.usefulness)/(rc-1)
        rating_avg.lecture_quality = (lq*rc - rank_to_delete.lecture_quality)/(rc-1)
        rating_avg.overall_quality = (oq*rc - rank_to_delete.overall_quality)/(rc-1)
        rating_avg.oral_written_tests_helpful = (owth*rc - rank_to_delete.oral_written_tests_helpful)/(rc-1)
        rating_avg.learned_much_info = (lmi*rc - rank_to_delete.learned_much_info)/(rc-1)
        rating_avg.rating_count = rc-1
        rating_avg.save()

    rank_to_delete.delete()  

    
    
    return redirect('history')

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

def search(request):
    ratings = None
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            course = form.cleaned_data.get("course")
            faculty = form.cleaned_data.get("faculty")
            course_faculty = Course_Faculty_Table.objects.filter(course__coursenumber__contains=course, faculty__facultyname__contains=faculty)
            order_by = request.GET.get('order_by', 'usefulness')
            ratings = Rating_Average.objects.filter(course_faculty__in=course_faculty).order_by("-"+order_by)
    else:
        form = SearchForm()
    return render(request, 'search.html', {'form':form, 'rating_average': ratings}) 

