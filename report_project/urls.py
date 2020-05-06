from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('report_app.urls')),
    path('api/accounts/', include('accounts_app.urls')),

]
