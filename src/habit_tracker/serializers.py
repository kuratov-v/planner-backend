from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            "id",
            "title",
            "description",
            "is_complete",
            "do_on_weekdays",
            "user",
            "date_created",
        ]
