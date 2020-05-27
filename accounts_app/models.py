from django.db import models
from secrets import token_urlsafe
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20,
                            choices=[('developer', 'developer'), ('validator', 'validator'), ('owner', 'owner')])

    def __str__(self):
        return f'{self.user}'


class PasswordResetRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=43, default=token_urlsafe)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.created_timestamp} - {self.updated_timestamp} - {self.token}'
