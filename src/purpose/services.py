from django.db.models import Sum, Avg, Max, Min
from typing import List

from .models import Purpose, PurposeResult, PurposeStatus


def _get_status_value(purpose: Purpose, result: List) -> int:
    if not result:
        return 0
    param = {
        "sum": sum,
        "avg": lambda x: sum(x) / len(x),
        "max": min if purpose.invert_value else max,
    }
    return param.get(purpose.mode)(result)


def get_purpose_results(purpose: Purpose) -> PurposeResult:
    param = {
        "sum": Sum,
        "avg": Avg,
        "min": Min,
        "max": Max,
    }
    purpose_result = PurposeResult.objects.filter(purpose=purpose)
    if not purpose.group_result_by:
        return PurposeResult.objects.filter(purpose=purpose)
    return (
        purpose_result.values(f"date__{purpose.group_result_by}")
        .annotate(value=param.get(purpose.group_result_mode)("value"))
        .order_by()
    )


def update_purpose_status(purpose: Purpose) -> None:
    purpose_status, _ = PurposeStatus.objects.get_or_create(purpose=purpose)
    result = get_purpose_results(purpose).values_list("value", flat=True)
    purpose_status.value = _get_status_value(purpose, result)
    purpose_status.save()
