from rest_framework import serializers
from .models import User
from .models import Profile
from .models import PasswordResetRequest


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user', 'role')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'profile', 'first_name', 'last_name', 'email', 'password')


class PasswordResetRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordResetRequest
        fields = ('id', 'user', 'token', 'created_timestamp', 'updated_timestamp')
