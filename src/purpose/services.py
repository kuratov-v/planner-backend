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
    if purpose.group_result_by:
        date_val = f"date__{purpose.group_result_by}"
        purpose_result = (
            purpose_result.values(date_val)
            .annotate(value=param.get(purpose.group_result_mode)("value"))
            .order_by()
        )
    return [
        {"date": res.get(date_val), "value": res.get("value")} for res in purpose_result
    ]


def update_purpose_status(purpose: Purpose) -> None:
    purpose_status, _ = PurposeStatus.objects.get_or_create(purpose=purpose)
    result = [res.get("value") for res in get_purpose_results(purpose)]
    purpose_status.value = _get_status_value(purpose, result)
    purpose_status.save()
