from django.db import models
from django.contrib.auth import get_user_model


class Habit(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    is_track_value = models.BooleanField(default=False)
    value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False)


class HabitComplete(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)
    date = models.DateField()
    value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
