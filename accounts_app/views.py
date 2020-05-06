from django.shortcuts import render, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.http import HttpResponseRedirect
from .models import PasswordResetRequest
import django_rq
from .messaging import email_message


def login(request):
    context = {}

    if request.method == "POST":
        user = authenticate(request, username=request.POST['user'], password=request.POST['password'])
        if user:
            dj_login(request, user)
            return HttpResponseRedirect(reverse('report_app:index'))
        else:
            context = {
                'error': 'Wrong username or password.'
            }
    return render(request, 'accounts_app/login.html', context)


def logout(request):
    dj_logout(request)
    return render(request, 'accounts_app/login.html')


def request_password_reset(request):
    if request.method == "POST":
        post_user = request.POST['username']
        user = None

        if post_user:
            try:
                user = User.objects.get(username=post_user)
            except:
                print(f"Invalid password request: {post_user}")
        else:
            post_user = request.POST['email']
            try:
                user = User.objects.get(email=post_user)
            except:
                print(f"Invalid password request: {post_user}")
        if user:
            prr = PasswordResetRequest()
            prr.user = user
            prr.save()
            django_rq.enqueue(email_message, {
                'token': prr.token,
                'email': prr.user.email,
            })
            return HttpResponseRedirect(reverse('accounts_app:password_reset'))

    return render(request, 'accounts_app/request_password_reset.html')


def password_reset(request):
    if request.method == "POST":
        post_user = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        token = request.POST['token']

        if password == confirm_password:
            try:
                prr = PasswordResetRequest.objects.get(token=token)
                prr.save()
            except:
                print("Invalid password reset attempt.")
                return render(request, 'accounts_app/password_reset.html')

            user = prr.user
            user.set_password(password)
            user.save()
            return HttpResponseRedirect(reverse('accounts_app:login'))

    return render(request, 'accounts_app/password_reset.html')


