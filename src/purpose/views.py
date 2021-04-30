from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import Purpose, PurposeResult, PurposeStatus
from .serializers import (
    PurposeSerializer,
    PurposeStatusSerializer,
    PurposeResultSerializer,
)


class PurposeViewSet(viewsets.ModelViewSet):
    serializer_class = PurposeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Purpose.objects.filter(user=self.request.user).select_related("status")

    def perform_create(self, serializer):
        serializer.validated_data["user"] = self.request.user
        return super(PurposeViewSet, self).perform_create(serializer)


class PurposeResultViewSet(viewsets.ModelViewSet):
    serializer_class = PurposeResultSerializer
    permission_classes = [IsAuthenticated]
    purpose_lookup = "purpose_id"
    purposes_lookup = f"{purpose_lookup}__in"
    parent_lookup = f"parent_lookup_{purpose_lookup}"

    def get_queryset(self):
        return PurposeResult.objects.filter(purpose_id=self.kwargs[self.parent_lookup])

    def perform_create(self, serializer):
        purpose = Purpose.objects.get(pk=self.kwargs[self.parent_lookup])
        serializer.validated_data["purpose"] = purpose
        return super(PurposeResultViewSet, self).perform_create(serializer)


class PurposeStatusViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    purpose_lookup = "purpose_id"
    purposes_lookup = f"{purpose_lookup}__in"
    parent_lookup = f"parent_lookup_{purpose_lookup}"
    permission_classes = [IsAuthenticated]
    serializer_class = PurposeStatusSerializer

    def get_queryset(self):
        return PurposeStatus.objects.filter(purpose_id=self.kwargs[self.parent_lookup])

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset:
            return None

        serializer = self.get_serializer(queryset[0], many=False)
        return Response(serializer.data)
