from django.db.models import Sum, Avg, Max, Min
from typing import List
from datetime import datetime, timedelta, date
import calendar

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


def _get_purpose_filter(group_by: str) -> List[str]:
    ranges = ["month", "year"]
    if group_by not in ranges:
        ranges.append(group_by)
    return [f"date__{r}" for r in ranges]


def get_week_range(year, week):
    first_day = datetime.strptime(f"{year}-W{week}-1", "%Y-W%W-%w").date()
    last_day = first_day + timedelta(days=6)
    return first_day, last_day


def _get_date(purpose: Purpose) -> str:
    year = int(purpose.get("date__year"))
    month = int(purpose.get("date__month"))
    week = int(purpose.get("date__week") or 0)
    day = int(purpose.get("date__day") or 0)
    fmt = "%d.%m.%Y"
    if day:
        d = date(year, month, day)
        return d.strftime(fmt)
    if week:
        first_day, last_day = get_week_range(year, week)
        return f"{first_day.strftime(fmt)} - {last_day.strftime(fmt)}"
    first_day = date(year, month, 1)
    last_day = date(year, month, calendar.monthrange(year, month)[1])
    return f"{first_day.strftime(fmt)} - {last_day.strftime(fmt)}"


def get_purpose_results(purpose: Purpose) -> PurposeResult:
    param = {
        "sum": Sum,
        "avg": Avg,
        "min": Min,
        "max": Max,
    }
    purpose_result = PurposeResult.objects.filter(purpose=purpose).order_by("date")
    if not purpose.group_result_by:
        return [
            {"date": res.date.strftime("%d.%m.%Y"), "value": res.value}
            for res in purpose_result
        ]
    purpose_filter = _get_purpose_filter(purpose.group_result_by)
    purpose_result = (
        purpose_result.values(*purpose_filter)
        .annotate(value=param.get(purpose.group_result_mode)("value"))
        .order_by()
    )
    return [
        {"date": _get_date(res), "value": "{0:.2f}".format(res.get("value"))}
        for res in purpose_result
    ]


def update_purpose_status(purpose: Purpose) -> None:
    purpose_status, _ = PurposeStatus.objects.get_or_create(purpose=purpose)
    result = [float(res.get("value")) for res in get_purpose_results(purpose)]
    purpose_status.value = _get_status_value(purpose, result)
    purpose_status.save()
