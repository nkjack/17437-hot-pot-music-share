import json
import os
from json import JSONDecodeError
from django.contrib.auth.models import User

# import spotipy
# import spotipy.util as util

from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.db import transaction

from hot_pot_music_share.models import *
from hot_pot_music_share.forms import *

#send mail
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

# Home view
@login_required
def home(request, username):
    context = {'title': 'home', 'error':''}
    context['username'] =  username
    user_from_url = get_object_or_404(User, username = username)
    
    if(request.method == "GET"):
        context['form'] = RoomForm(initial={'owner': request.user})

        popular_rooms = Room.objects.all().order_by('thumbs_up')[:6]
        context["popular"] = popular_rooms

        print(popular_rooms)
        return render(request, 'home.html', context)

    elif (request.POST.get('create_room')):
        form = RoomForm(request.POST, request.FILES, initial={'owner': request.user})
        context['form'] = form

        if form.is_valid():
            print("0kkkk")
            new_room = Room.objects.create(owner = request.user,
                                            name = form.cleaned_data['name'],
                                            description = form.cleaned_data['description'],
                                            cover_pic = form.cleaned_data['cover_pic']
                                            )
            new_room.save()
            new_history = RoomHistory.objects.create(user = request.user, 
                                                        visited_room = new_room)
            new_history.save()

            return HttpResponseRedirect(reverse('room',args = [new_room.pk]))
        else:

            return render(request, 'home.html', context)

    else:
        context['error'] = "Please press Submit button to create a new room"

        return render(request, 'home.html', context)

# Integrate actual Profile model later
def customLogin(request):
    context = {'login_active':'active', 'register_active':'',}
    # If already logged in, redirect to home
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home',args=[request.user.username]))

    if request.method =='GET':
        context['login_form'] = LoginForm()
        
        return render(request, 'login.html', context)

    if request.POST.get('login'):
        form = LoginForm(request.POST)
        context['login_form'] = form

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            
            user = authenticate(request, username = username, password = password)
            
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home',args=[username]))
            else:
                context['error'] = 'Invalid login. Password doesnot match the user or user doesnot exist'
                return render(request, 'login.html', context)
        else:
            return render(request, 'login.html', context)

    
    elif 'resetPassword' in request.POST or request.POST['resetPassword']:
        return HttpResponseRedirect(reverse('forgetPassword'))


    else:
        context['error'] = "Please press Login button to register an account"
        return render(request, 'login.html', context)


def register(request):
    context = {'register_active': 'active', 'login_active' : ''}

    if request.method =='GET':
        context['registration_form'] = RegistrationForm()
    
        return render(request, 'login.html', context)
    else:
        if 'register' in request.POST or request.POST['register']:
            form = RegistrationForm(request.POST)
            context['registration_form'] = form 
            if form.is_valid():
                new_user = User.objects.create_user(username = form.cleaned_data['username'],
                                                    password = form.cleaned_data['password1'],                                         
                                                    email = form.cleaned_data['email'])

                new_user.is_active = False
                new_user.save()

                token = default_token_generator.make_token(new_user)
                email_body = """
                Welcome to hot_pot_music_share. Please click the link below to verify your email address and complete registration:
                http://%s%s
                """ % (request.get_host(),
                    reverse('confirm', args=(new_user.username, token)))

                send_mail(subject = "Verify Your Email Adress",
                        message = email_body,
                        from_email = "..",
                        recipient_list = [new_user.email])

                context["email"] = "Welcome to Hot Pot Music Share. Please check your mailbox to find verification link to complete registration"
                return render(request,'email_confirmation.html',context)

                # login(request, new_user)
                # return HttpResponseRedirect(reverse('home',args=[new_user.username]))
            else:
                context['error'] = "Please check if all the field satisfy requirements or the username is already taken"
                return render(request, 'login.html', context)
        else:
            context['error'] = "Please press Register button to register an account"
            return render(request, 'login.html', context)

def customLogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@transaction.atomic
def confirm_email(request, username, token):
    user = get_object_or_404(User, username = username)
    if default_token_generator.check_token(user,token):

        user.is_active = True
        user.save()

        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponse('Invalid Link')


@login_required
def room(request, pk):

    context ={'username' : request.user.username}
    # if request.method =='GET':


    return render(request, 'room_base.html', context)

@login_required
def history(request):
    context = {'owned':'','visited':'', 'username':request.user.username}
    if request.method =='GET':
        owned = Room.objects.filter(owner = request.user)
        visited = RoomHistory.getVistedRooms(request.user)

        context['owned'] = owned
        context['visited'] = visited

    return render(request, 'room_history.html', context)

