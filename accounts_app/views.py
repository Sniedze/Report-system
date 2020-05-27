from django.shortcuts import render, reverse
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate,  logout as dj_logout
from django.http import HttpResponseRedirect
from .models import PasswordResetRequest
import django_rq
from .messaging import email_message
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from .serializers import UserSerializer, ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UsersViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token': token.key, 'user_id': user.id},
                    status=HTTP_200_OK)


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
