from rest_framework import serializers
from .models import Purpose, PurposeResult, PurposeStatus


class PurposeSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Purpose
        fields = [
            "id",
            "name",
            "description",
            "end_value",
            "end_date",
            "date_created",
            "mode",
            "invert_value",
            "is_complete",
            "user",
            "status",
            "group_result_by",
            "group_result_mode",
        ]

    def get_status(self, obj):
        return obj.status.value


class PurposeResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurposeResult
        fields = "__all__"
        read_only_fields = ("purpose",)


class PurposeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurposeStatus
        fields = "__all__"
