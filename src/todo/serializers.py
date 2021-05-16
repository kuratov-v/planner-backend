from rest_framework import serializers
from .models import Project, Task, CheckList, Item, Section


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "user", "date_created"]


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TaskReadSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "section",
            "title",
            "description",
            "date_created",
            "is_complete",
            "date",
            "time",
        ]

    def get_time(self, obj):
        if obj.time and obj.date:
            return obj.time.strftime("%H:%M")
        return None


class CheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckList
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"
