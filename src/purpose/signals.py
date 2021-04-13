from .models import Purpose, PurposeResult
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from . import services


@receiver(post_save, sender=Purpose)
def purpose_save(sender, instance, *args, **kwargs):
    services.update_purpose_status(instance)


@receiver(post_save, sender=PurposeResult)
def purpose_result_save(sender, instance, *args, **kwargs):
    services.update_purpose_status(instance.purpose)


@receiver(post_delete, sender=PurposeResult)
def purpose_result_delete(sender, instance, *args, **kwargs):
    services.update_purpose_status(instance.purpose)
