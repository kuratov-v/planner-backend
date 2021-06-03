from django.db import models

from django.contrib.auth import get_user_model
from django.utils import timezone


class BudgetBoard(models.Model):
    name = models.CharField(max_length=250)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False)


class BudgetBoardUser(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    budget_board = models.ForeignKey(BudgetBoard, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=50)
    budget_board = models.ForeignKey(BudgetBoard, on_delete=models.CASCADE)


class Transaction(models.Model):
    name = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    budget_board = models.ForeignKey(
        BudgetBoard, on_delete=models.CASCADE, related_name="transactions"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="transactions",
    )
    date = models.DateField()

    @property
    def status(self):
        return "expense" if self.amount < 0 else "profit"

    class Meta:
        ordering = ["-date"]
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
