from django.contrib import admin
from django.urls import path, include
from .api import router

urlpatterns = [
    path('', include('report_app.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts_app.urls')),
    path('api/', include(router.urls)),
    ]
