from rest_framework import serializers
from .models import Report


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('id', 'title', 'description', 'category', "status",)
