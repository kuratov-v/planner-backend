from django.db import models
from django.contrib.auth import get_user_model


class Purpose(models.Model):
    MODE = (
        ("sum", "Сумма"),
        ("avg", "Среднее значение"),
        ("max", "Максимальное значение"),
    )
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, blank=True, null=True)
    end_value = models.DecimalField(max_digits=20, decimal_places=2)
    end_date = models.DateField(blank=True, null=True)
    mode = models.CharField(choices=MODE, max_length=3)
    invert_value = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False)


class PurposeResult(models.Model):
    purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.DecimalField(max_digits=20, decimal_places=2)


class PurposeStatus(models.Model):
    purpose = models.OneToOneField(Purpose, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=20, decimal_places=2, null=True, default=0)
