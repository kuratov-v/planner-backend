from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField


class Habit(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150, null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False)
    is_complete = models.BooleanField(default=False)
    do_on_weekdays = ArrayField(models.PositiveSmallIntegerField())
    date_created = models.DateField(auto_now_add=True)


class HabitCompleteDay(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False, blank=True, null=True)
    date = models.DateField()
