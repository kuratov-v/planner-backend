from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from .models import BudgetBoard, Transaction, Category
from .serializers import (
    BudgetBoardSerializer,
    TransactionReadSerializer,
    TransactionEditSerializer,
    CategorySerializer,
)


class BudgetBoardViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetBoardSerializer
    budget_board_lookup = "budget_board_id"
    budget_boards_lookup = f"{budget_board_lookup}__in"
    parent_org_lookup = f"parent_lookup_{budget_board_lookup}"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BudgetBoard.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.validated_data["user"] = self.request.user
        return super(BudgetBoardViewSet, self).perform_create(serializer)


class TransactionViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    budget_board_lookup = "budget_board_id"
    budget_boards_lookup = f"{budget_board_lookup}__in"
    parent_org_lookup = f"parent_lookup_{budget_board_lookup}"
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TransactionReadSerializer
        return TransactionEditSerializer

    def get_queryset(self):
        return Transaction.objects.filter(
            budget_board_id=self.kwargs[self.parent_org_lookup]
        )

    def list(self, request, *args, **kwargs):
        results = self.get_queryset()

        # TODO: refactor filters
        params = request.query_params
        if params.get("date_from"):
            results = results.filter(date__gte=params.get("date_from"))
        if params.get("date_to"):
            results = results.filter(date__lte=params.get("date_to"))
        if params.get("status"):
            results = results.filter(status=params.get("status"))
        if params.get("category"):
            results = results.filter(category_id__in=params.getlist("category"))

        serializer = TransactionReadSerializer(results, many=True)
        return Response(serializer.data)


class CategoryViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    budget_board_lookup = "budget_board_id"
    budget_boards_lookup = f"{budget_board_lookup}__in"
    parent_org_lookup = f"parent_lookup_{budget_board_lookup}"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(
            budget_board_id=self.kwargs[self.parent_org_lookup]
        )
