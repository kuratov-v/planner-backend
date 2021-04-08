from django.db import models

from django.contrib.auth import get_user_model
from django.utils import timezone


class BudgetBoard(models.Model):
    name = models.CharField(max_length=250)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, editable=False)


class BudgetBoardUser(models.Model):
    RIGHTS = (
        ("read", "Чтение"),
        ("write", "изменение"),
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    budget_board = models.ForeignKey(BudgetBoard, on_delete=models.CASCADE)
    rights = models.CharField(max_length=5, choices=RIGHTS, default="guest")


class Category(models.Model):
    name = models.CharField(max_length=50)
    budget_board = models.ForeignKey(BudgetBoard, on_delete=models.CASCADE)


class Transaction(models.Model):
    STATUS = (
        ("expense", "Расход"),
        ("profit", "Доход"),
    )
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
    status = models.CharField(max_length=10, choices=STATUS, default="profit")
    date = models.DateField()

    class Meta:
        ordering = [
            "-date",
        ]
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
