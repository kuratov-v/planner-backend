from django.test import TestCase

from src.purpose.models import Purpose, PurposeResult
from src.purpose.services import get_purpose_results
from django.contrib.auth import get_user_model


class GetPurposeResultsTest(TestCase):
    def setUp(self):
        self.user_1 = get_user_model().objects.create(username="test_user")

        self.purpose = Purpose.objects.create(
            name="Sum purpose",
            end_value="1000",
            end_date="2050-12-12",
            mode="sum",
            user=self.user_1,
        )
        self.result_1 = PurposeResult.objects.create(
            purpose=self.purpose,
            date="2021-03-01",
            value=200,
        )
        self.result_2 = PurposeResult.objects.create(
            purpose=self.purpose,
            date="2021-03-08",
            value=-300,
        )
        self.result_3 = PurposeResult.objects.create(
            purpose=self.purpose,
            date="2021-03-10",
            value=500,
        )
        self.result_4 = PurposeResult.objects.create(
            purpose=self.purpose,
            date="2021-04-10",
            value=1000,
        )
        self.result_5 = PurposeResult.objects.create(
            purpose=self.purpose,
            date="2021-04-10",
            value=100,
        )

    def test_without_gorup_result(self):
        purpose_results = get_purpose_results(self.purpose)
        expected_data = [
            {"date": "01.03.2021", "value": 200.00},
            {"date": "08.03.2021", "value": -300.00},
            {"date": "10.03.2021", "value": 500.00},
            {"date": "10.04.2021", "value": 1000.00},
            {"date": "10.04.2021", "value": 100.00},
        ]
        self.assertEqual(expected_data, purpose_results)

    def test_sum_day(self):
        self.purpose.group_result_by = "day"
        self.purpose.group_result_mode = "sum"
        self.purpose.save()
        purpose_results = get_purpose_results(self.purpose)
        expected_data = [
            {"date": "01.03.2021", "value": "200.00"},
            {"date": "08.03.2021", "value": "-300.00"},
            {"date": "10.03.2021", "value": "500.00"},
            {"date": "10.04.2021", "value": "1100.00"},
        ]
        self.assertEqual(expected_data, purpose_results)

    def test_sum_week(self):
        self.purpose.group_result_by = "week"
        self.purpose.group_result_mode = "sum"
        self.purpose.save()
        purpose_results = get_purpose_results(self.purpose)
        expected_data = [
            {"date": "01.03.2021 - 07.03.2021", "value": "200.00"},
            {"date": "08.03.2021 - 14.03.2021", "value": "200.00"},
            {"date": "05.04.2021 - 11.04.2021", "value": "1100.00"},
        ]
        self.assertEqual(expected_data, purpose_results)

    def test_sum_month(self):
        self.purpose.group_result_by = "month"
        self.purpose.group_result_mode = "sum"
        self.purpose.save()
        purpose_results = get_purpose_results(self.purpose)
        expected_data = [
            {"date": "01.03.2021 - 31.03.2021", "value": "400.00"},
            {"date": "01.04.2021 - 30.04.2021", "value": "1100.00"},
        ]
        self.assertEqual(expected_data, purpose_results)

    def test_avg_day(self):
        self.purpose.group_result_by = "day"
        self.purpose.group_result_mode = "avg"
        self.purpose.save()
        purpose_results = get_purpose_results(self.purpose)
        expected_data = [
            {"date": "01.03.2021", "value": "200.00"},
            {"date": "08.03.2021", "value": "-300.00"},
            {"date": "10.03.2021", "value": "500.00"},
            {"date": "10.04.2021", "value": "550.00"},
        ]
        self.assertEqual(expected_data, purpose_results)

    def test_avg_week(self):
        self.purpose.group_result_by = "week"
        self.purpose.group_result_mode = "avg"
        self.purpose.save()
        purpose_results = get_purpose_results(self.purpose)
        expected_data = [
            {"date": "01.03.2021 - 07.03.2021", "value": "200.00"},
            {"date": "08.03.2021 - 14.03.2021", "value": "100.00"},
            {"date": "05.04.2021 - 11.04.2021", "value": "550.00"},
        ]
        self.assertEqual(expected_data, purpose_results)

    def test_avg_month(self):
        self.purpose.group_result_by = "month"
        self.purpose.group_result_mode = "avg"
        self.purpose.save()
        purpose_results = get_purpose_results(self.purpose)
        expected_data = [
            {"date": "01.03.2021 - 31.03.2021", "value": "133.33"},
            {"date": "01.04.2021 - 30.04.2021", "value": "550.00"},
        ]
        self.assertEqual(expected_data, purpose_results)

    def test_max_day(self):
        self.purpose.group_result_by = "day"
        self.purpose.group_result_mode = "max"
        self.purpose.save()
        purpose_results = get_purpose_results(self.purpose)
        expected_data = [
            {"date": "01.03.2021", "value": "200.00"},
            {"date": "08.03.2021", "value": "-300.00"},
            {"date": "10.03.2021", "value": "500.00"},
            {"date": "10.04.2021", "value": "1000.00"},
        ]
        self.assertEqual(expected_data, purpose_results)

    def test_max_week(self):
        self.purpose.group_result_by = "week"
        self.purpose.group_result_mode = "max"
        self.purpose.save()
        purpose_results = get_purpose_results(self.purpose)
        expected_data = [
            {"date": "01.03.2021 - 07.03.2021", "value": "200.00"},
            {"date": "08.03.2021 - 14.03.2021", "value": "500.00"},
            {"date": "05.04.2021 - 11.04.2021", "value": "1000.00"},
        ]
        self.assertEqual(expected_data, purpose_results)

    def test_max_month(self):
        self.purpose.group_result_by = "month"
        self.purpose.group_result_mode = "max"
        self.purpose.save()
        purpose_results = get_purpose_results(self.purpose)
        expected_data = [
            {"date": "01.03.2021 - 31.03.2021", "value": "500.00"},
            {"date": "01.04.2021 - 30.04.2021", "value": "1000.00"},
        ]
        self.assertEqual(expected_data, purpose_results)
