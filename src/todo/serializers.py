from rest_framework import serializers
from .models import Project, Task, CheckList, Item, Section


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "user",
            "date_created",
            "is_hide_complete",
        ]


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
    check_list = serializers.SerializerMethodField()

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
            "check_list",
        ]

    def get_time(self, obj):
        if obj.time and obj.date:
            return obj.time.strftime("%H:%M")
        return None

    def get_check_list(self, obj):
        items = Item.objects.filter(check_list__task=obj)
        if not items:
            return None
        complete_items = items.filter(is_complete=True)
        return f"{complete_items.count()}/{items.count()}"


class CheckListSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = CheckList
        fields = [
            "id",
            "title",
            "task",
            "is_hide_complete",
            "items",
        ]

    def get_items(self, obj):
        items = obj.items.all()
        return ItemSerializer(items, many=True).data


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "title", "check_list", "is_complete"]
