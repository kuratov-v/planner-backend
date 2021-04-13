from django.db.models import Sum, Avg, Max, Min

from .models import Purpose, PurposeResult, PurposeStatus

        
def update_purpose_status(purpose: Purpose) -> None:
    purpose_status, _ = PurposeStatus.objects.get_or_create(purpose=purpose)
    purpose_result = PurposeResult.objects.filter(purpose=purpose)
    if purpose.mode == "sum":
        purpose_status.value = purpose_result.aggregate(Sum("value")).get("value__sum")
    elif purpose.mode == "avg":
        purpose_status.value = purpose_result.aggregate(Avg("value")).get("value__avg")
    elif purpose.mode == "max" and purpose.invert_value:
        purpose_status.value = purpose_result.aggregate(Min("value")).get("value__min")
    elif purpose.mode == "max" and not purpose.invert_value:
        purpose_status.value = purpose_result.aggregate(Max("value")).get("value__max")
    purpose_status.save()
