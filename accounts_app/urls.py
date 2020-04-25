from django.urls import path
from . import views

app_name = 'accounts_app'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('request_password_reset/', views.request_password_reset, name='request_password_reset'),
    path('password_reset/', views.password_reset, name='password_reset'),
]
