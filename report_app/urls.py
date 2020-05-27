from django.urls import path, include
from . import views

app_name = 'report_app'

urlpatterns = [
    # path('', views.ReportView.as_view()),
    path('reports/', views.UsersReportView.as_view()),
    path('reports/<int:pk>/', views.ReportDetail.as_view()),

]
