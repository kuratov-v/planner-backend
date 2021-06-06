from rest_framework import status
from rest_framework.test import APITestCase

from src.budget.models import BudgetBoard, Category, Transaction

from src.budget.serializers import (
    BudgetBoardSerializer,
    CategorySerializer,
    TransactionReadSerializer,
)
from django.contrib.auth import get_user_model


class BudgetAPITestCase(APITestCase):
    def setUp(self):
        self.user_1 = get_user_model().objects.create(username="test_username_1")
        self.user_2 = get_user_model().objects.create(username="test_username_2")

        self.board_1 = BudgetBoard.objects.create(name="Board 1", user=self.user_1)
        self.board_2 = BudgetBoard.objects.create(name="Board 2", user=self.user_2)

        self.category_1 = Category.objects.create(
            budget_board=self.board_1,
            name="category 1",
        )
        self.category_2 = Category.objects.create(
            budget_board=self.board_1,
            name="category 2",
        )
        self.category_3 = Category.objects.create(
            budget_board=self.board_2,
            name="category 3",
        )

        self.transaction_1 = Transaction.objects.create(
            name="Tr1",
            amount=220,
            budget_board=self.board_1,
            category=self.category_1,
            date="2020-12-12",
        )
        self.transaction_2 = Transaction.objects.create(
            name="Tr2",
            amount=-120,
            budget_board=self.board_1,
            category=self.category_1,
            date="2020-12-12",
        )
        self.transaction_3 = Transaction.objects.create(
            name="Tr3",
            amount=120,
            budget_board=self.board_2,
            category=self.category_3,
            date="2020-10-10",
        )
        self.transaction_4 = Transaction.objects.create(
            name="Tr4",
            amount=120,
            budget_board=self.board_1,
            category=self.category_2,
            date="2020-11-11",
        )


class BudgetBoardAPITestCase(BudgetAPITestCase):
    def test_get_board(self):
        self.client.force_authenticate(user=self.user_1)
        response = self.client.get(f"/api/v1/budget-board/{self.board_1.id}/")
        expected_data = BudgetBoardSerializer(self.board_1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

        self.client.force_authenticate(user=self.user_2)
        response = self.client.get(f"/api/v1/budget-board/{self.board_1.id}/")
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_get_boards(self):
        response = self.client.get("/api/v1/budget-board/")
        expected_data = BudgetBoardSerializer(self.board_1).data
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        self.client.force_authenticate(user=self.user_1)
        response = self.client.get("/api/v1/budget-board/")
        expected_data = BudgetBoardSerializer([self.board_1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_create_board(self):
        self.client.force_authenticate(user=self.user_1)
        data = {"name": "new board"}
        response = self.client.post("/api/v1/budget-board/", data=data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        response_get = self.client.get(
            f"/api/v1/budget-board/{response.data.get('id')}/"
        )
        self.assertEqual(status.HTTP_200_OK, response_get.status_code)
        self.assertEqual(response.data.get("id"), response_get.data.get("id"))
        self.assertEqual("new board", response_get.data.get("name"))

    def test_update_board(self):
        self.client.force_authenticate(user=self.user_1)
        data = {"name": "board_renamed"}
        response = self.client.patch(
            f"/api/v1/budget-board/{self.board_1.id}/",
            data=data,
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        response_get = self.client.get(f"/api/v1/budget-board/{self.board_1.id}/")
        self.assertEqual(status.HTTP_200_OK, response_get.status_code)
        self.assertEqual("board_renamed", response_get.data.get("name"))

    def test_delete_board(self):
        self.client.force_authenticate(user=self.user_1)
        response = self.client.delete(f"/api/v1/budget-board/{self.board_1.id}/")
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        response_get = self.client.get(f"/api/v1/budget-board/{self.board_1.id}/")
        self.assertEqual(status.HTTP_404_NOT_FOUND, response_get.status_code)


class CategoryAPITestCase(BudgetAPITestCase):
    def test_get_categories(self):
        self.client.force_authenticate(user=self.user_1)
        url = f"/api/v1/budget-board/{self.board_1.id}/categories/"
        response = self.client.get(url)
        expected_data = CategorySerializer(
            [self.category_1, self.category_2],
            many=True,
        ).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)

    def test_create_category(self):
        self.client.force_authenticate(user=self.user_1)
        board_id = self.board_1.id
        data = {"budget_board": board_id, "name": "new category"}
        response = self.client.post(
            f"/api/v1/budget-board/{board_id}/categories/",
            data=data,
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        response_get = self.client.get(f"/api/v1/budget-board/{board_id}/categories/")
        self.assertEqual(status.HTTP_200_OK, response_get.status_code)
        self.assertEqual(3, len(response_get.data))

    def test_update_category(self):
        self.client.force_authenticate(user=self.user_1)
        url = f"/api/v1/budget-board/{self.board_1.id}/categories/{self.category_2.id}/"
        response = self.client.patch(url, data={"name": "category_renamed"})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        response_get = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response_get.status_code)
        self.assertEqual("category_renamed", response.data.get("name"))

    def test_delete_category(self):
        self.client.force_authenticate(user=self.user_1)
        url = f"/api/v1/budget-board/{self.board_1.id}/categories/{self.category_2.id}/"
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        response_get = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response_get.status_code)


class TransactionAPITestCase(BudgetAPITestCase):
    def test_get_transaction(self):
        self.client.force_authenticate(user=self.user_1)
        url = f"/api/v1/budget-board/{self.board_1.id}/transactions/{self.transaction_2.id}/"
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("expense", response.data.get("status"))
        self.assertEqual("120.00", response.data.get("amount"))

    def test_get_transactions(self):
        self.client.force_authenticate(user=self.user_1)
        url = f"/api/v1/budget-board/{self.board_1.id}/transactions/"
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, len(response.data))

        url = f"/api/v1/budget-board/{self.board_1.id}/transactions/{self.transaction_3.id}/"
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_create_transaction(self):
        self.client.force_authenticate(user=self.user_1)
        board_id = self.board_1.id
        data = {
            "name": "new tr",
            "date": "2020-12-12",
            "category": self.category_2.id,
            "amount": -200,
            "budget_board": board_id,
        }
        response = self.client.post(
            f"/api/v1/budget-board/{board_id}/transactions/",
            data=data,
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        response_get = self.client.get(f"/api/v1/budget-board/{board_id}/transactions/")
        self.assertEqual(status.HTTP_200_OK, response_get.status_code)
        self.assertEqual(4, len(response_get.data))

    def test_update_transaction(self):
        self.client.force_authenticate(user=self.user_1)
        url = f"/api/v1/budget-board/{self.board_1.id}/transactions/{self.transaction_4.id}/"
        response = self.client.patch(url, data={"amount": -200})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        response_get = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response_get.status_code)
        self.assertEqual("200.00", response_get.data.get("amount"))
        self.assertEqual("expense", response_get.data.get("status"))

    def test_delete_transaction(self):
        self.client.force_authenticate(user=self.user_1)
        url = f"/api/v1/budget-board/{self.board_1.id}/transactions/{self.transaction_4.id}/"
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        response_get = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response_get.status_code)
