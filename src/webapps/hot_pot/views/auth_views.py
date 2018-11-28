from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from hot_pot.forms import LoginForm, RegistrationForm, UsernameForm,PasswordForm


def register(request):
    context = {'register_active': 'active', 'login_active': ''}

    if request.method == 'GET':
        context['registration_form'] = RegistrationForm()

        return render(request, 'user_auth/login.html', context)
    else:
        if 'register' in request.POST or request.POST['register']:
            form = RegistrationForm(request.POST)
            context['registration_form'] = form
            if form.is_valid():
                new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                                    password=form.cleaned_data['password1'],
                                                    email=form.cleaned_data['email'])

                new_user.is_active = False
                new_user.save()

                token = default_token_generator.make_token(new_user)
                email_body = """
				Welcome to hot_pot. Please click the link below to verify your email address and complete registration:
				http://%s%s
				""" % (request.get_host(),
                       reverse('confirm', args=(new_user.username, token)))

                send_mail(subject="Verify Your Email Address",
                          message=email_body,
                          from_email="..",
                          recipient_list=[new_user.email])

                context["email"] = "Welcome to Hot Pot Music Share. Please check your mailbox to find verification " \
                                   "link to complete registration"
                return render(request, 'user_auth/email_confirmation.html', context)

            else:
                context['error'] = "Please check if all the field satisfy requirements or the username is already taken"
                return render(request, 'user_auth/login.html', context)
        else:
            context['error'] = "Please press Register button to register an account"
            return render(request, 'user_auth/login.html', context)


def custom_login(request):
    context = {'login_active': 'active', 'register_active': '', }
    # If already logged in, redirect to home
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home', args=[request.user.username]))

    if request.method == 'GET':
        context['login_form'] = LoginForm()

        return render(request, 'user_auth/login.html', context)

    if request.POST.get('login'):
        form = LoginForm(request.POST)
        context['login_form'] = form

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home', args=[username]))
            else:
                context['error'] = 'Invalid login. Password does not match the user or user does not exist'
                return render(request, 'user_auth/login.html', context)
        else:
            return render(request, 'user_auth/login.html', context)

    elif 'resetPassword' in request.POST or request.POST['resetPassword']:
        return HttpResponseRedirect(reverse('forgetPassword'))

    else:
        context['error'] = "Please press login button to register an account"
        return render(request, 'user_auth/login.html', context)


def custom_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@transaction.atomic
def confirm_email(request, username, token):
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, token):

        user.is_active = True
        user.save()

        return HttpResponseRedirect(reverse('login'))
    else:
        return HttpResponse('Invalid Link')


def forget_password(request):
    context = {'usernameForm' : ""}
    if request.method == 'GET':
        username_form = UsernameForm()
        context['usernameForm'] = username_form
        return render(request, 'user_auth/reset_password.html',context)
    else:
        if 'resetPassword' in request.POST or request.POST['resetPassword']:
            username_form = UsernameForm(request.POST)
            context['usernameForm'] = username_form

            if username_form.is_valid():
                username = request.POST['username']
                user = get_object_or_404(User, username = username)

                send_password_email(request, user)

                context["email"] = "Forget Your Password? Dont worry, check your mailbox and follow the instructions."
                return render(request,'user_auth/email_confirmation.html',context)
            else:

                return render(request, 'user_auth/reset_password.html',context)   

        else:
            context['error'] = "Please press Reset button to change your password"
            return render(request, 'user_auth/reset_password.html',context)





@transaction.atomic
def reset_password(request, username, token):
    
    user = get_object_or_404(User, username = username)
    if default_token_generator.check_token(user,token):

        context = {'password':''}
        if request.method == "GET":
            password_form = PasswordForm()
            context['password'] = password_form
            return render(request, 'user_auth/reset_password.html',context)
        else:
            if request.POST.get('resetPassword'):
                password_form = PasswordForm(request.POST)
                context['password'] = password_form

                if password_form.is_valid():
                    password = request.POST['password1']

                    user.set_password(password)
                    user.save()
                    login(request, user)
                    return HttpResponseRedirect(reverse('home',args=[user.username]))
                else:
                    return render(request, 'user_auth/reset_password.html',context)


            else:
                context['error'] = "Please press Reset button to change your password"
                return render(request, 'user_auth/reset_password.html',context)
        
    else:
        return HttpResponse('Invalid Link')


def send_password_email(request, user):

    token = default_token_generator.make_token(user)
    email_body = """
    Want to Reset Your Password? Dont worry, please follow the instructions :
    http://%s%s
    """ % (request.get_host(),
        reverse('resetPassword', args=(user.username, token)))

    send_mail(subject="Verify Your Email Address",
                          message=email_body,
                          from_email="..",
                          recipient_list=[user.email])

    return token