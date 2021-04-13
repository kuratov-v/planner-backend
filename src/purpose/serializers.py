from rest_framework import serializers
from .models import Purpose, PurposeResult, PurposeStatus


class PurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purpose
        fields = "__all__"


class PurposeResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurposeResult
        fields = "__all__"
        read_only_fields = ("purpose",)


class PurposeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurposeStatus
        fields = "__all__"
