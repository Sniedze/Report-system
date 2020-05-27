from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Report(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=[('market', 'Market Risk'), ('credit', 'Credit Risk'),
                                                        ('liquidity', 'Liquidity Risk'), ('pricing', 'Pricing Risk'),
                                                        ('compliance', 'Compliance Risk')])
    status = models.CharField(max_length=20, choices=[('created', 'Created'), ('validated', 'Validated'),
                                                      ('approved', 'Approved'), ('rejected', 'Rejected')])
    developer = models.ForeignKey(User, related_name='developer', on_delete=models.CASCADE)
    validator = models.ForeignKey(User, related_name='validator', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'


class Operation(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='operation')
    operation_name = models.CharField(max_length=20, choices=[('create', 'Create'), ('validate', 'Validate'),
                                                              ('approve', 'Approve'), ('reject', 'Reject')])
    date = models.DateField(default=datetime.today)

    def __str__(self):
        return f'{self.operation_name}'


class Risk(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='risk')
    risk_tier = models.CharField(max_length=6, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    risk_weight = models.CharField(max_length=6, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])

    def __str__(self):
        return f'{self.risk_tier}'
