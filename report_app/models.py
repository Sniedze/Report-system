from django.db import models
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class Report(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=[('market', 'Market Risk'), ('credit', 'Credit Risk'), ('liquidity', 'Liquidity Risk'), ('pricing', 'Pricing Risk'), ('compliance', 'Compliance Risk')])
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class AssignedUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.report} - {self.role}'


class Operation(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    operation_name = models.CharField(max_length=20)
    date = models.DateField(default=datetime.today)


class RiskAssessment:
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    risk_tier = models.DecimalField(decimal_places=1)
    risk_weight = models.DecimalField(decimal_places=1)

