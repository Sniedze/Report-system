from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Operation, Report


@receiver(post_save, sender=Report, dispatch_uid="create_operation")
def create_operation(sender, instance, created, **kwargs):
    if not Operation.objects.filter(report=instance).exists():
        operation = Operation()
        operation.report = instance
        operation.operation_name = "create"
        operation.save()
