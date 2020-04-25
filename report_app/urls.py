from django.urls import path, include
from . import views


app_name = 'report_app'

urlpatterns = [
    path('', views.index, name='index')
    ]

