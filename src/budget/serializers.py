from rest_framework import serializers
from .models import BudgetBoard, Transaction, Category


class BudgetBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetBoard
        fields = ["id", "name", "user"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class TransactionReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            "id",
            "name",
            "amount",
            "budget_board",
            "category",
            "date",
            "status",
        ]

    def get_amount(self, obj):
        return str(round(abs(obj.amount), 2))


class TransactionEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "name", "amount", "budget_board", "category", "date"]
