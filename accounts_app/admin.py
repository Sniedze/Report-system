from django.contrib import admin
from .models import UserProfile
from .models import PasswordResetRequest

admin.site.register(UserProfile)
admin.site.register(PasswordResetRequest)