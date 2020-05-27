from rest_framework import serializers
from .models import Report
from .models import Operation
from .models import Risk


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ('id', 'report', 'operation_name', 'date')


class RiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk
        fields = ('id', 'report', 'risk_tier', 'risk_weight')


class ReportSerializer(serializers.ModelSerializer):
    operation = serializers.StringRelatedField(many=True, read_only=True)
    risk = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Report
        fields = (
            'id', 'title', 'description', 'category', "status", "developer", "validator", "owner", "operation", "risk", "user")

    def create(self, validated_data):
        return Report.objects.create(**validated_data)
