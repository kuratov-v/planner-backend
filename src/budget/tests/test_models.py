from mixer.backend.django import mixer
import pytest


@pytest.mark.django_db
def test_transaction_expense():
    transaction = mixer.blend("budget.Transaction", amount=-100)
    assert transaction.status == "expense"


@pytest.mark.django_db
def test_transaction_profit():
    transaction = mixer.blend("budget.Transaction", amount=100)
    assert transaction.status == "profit"

    transaction = mixer.blend("budget.Transaction", amount=0)
    assert transaction.status == "profit"
