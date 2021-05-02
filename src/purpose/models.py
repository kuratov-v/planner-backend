from django.db import models
from django.contrib.auth import get_user_model


class Purpose(models.Model):
    MODE = (
        ("sum", "Сумма"),
        ("avg", "Среднее значение"),
        ("max", "Максимальное значение"),
    )
    RESULT_MODE = (
        ("sum", "Сумма"),
        ("avg", "Среднее значение"),
        ("max", "Максимальное значение"),
        ("min", "Минимальное значение"),
    )
    GROUP_MODE = (
        ("day", "День"),
        ("week", "Неделя"),
        ("month", "Месяц"),
    )
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, blank=True, null=True)
    end_value = models.DecimalField(max_digits=20, decimal_places=2)
    end_date = models.DateField(blank=True, null=True)
    date_created = models.DateField(auto_now_add=True, editable=False)
    mode = models.CharField(choices=MODE, max_length=3)
    invert_value = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False)
    group_result_mode = models.CharField(
        choices=RESULT_MODE, max_length=3, default="sum"
    )
    group_result_by = models.CharField(
        null=True, choices=GROUP_MODE, max_length=5, default=None
    )


class PurposeResult(models.Model):
    purpose = models.ForeignKey(
        Purpose, null=True, on_delete=models.SET_NULL, related_name="results"
    )
    date = models.DateField()
    value = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        ordering = ["-date"]


class PurposeStatus(models.Model):
    purpose = models.OneToOneField(
        Purpose, on_delete=models.CASCADE, related_name="status"
    )
    value = models.DecimalField(max_digits=20, decimal_places=2, null=True, default=0)
