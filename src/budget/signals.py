from .models import Transaction
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Transaction)
def check_transaction_amount(sender, instance, *args, **kwargs):
    if instance.amount < 0 and instance.status != "expense":
        instance.status = "expense"
        instance.save()
    elif instance.amount >= 0 and instance.status != "profit":
        instance.status = "profit"
        instance.save()
