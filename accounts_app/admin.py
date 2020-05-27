from django.contrib import admin
from .models import Profile, PasswordResetRequest

admin.site.register(Profile)
admin.site.register(PasswordResetRequest)
