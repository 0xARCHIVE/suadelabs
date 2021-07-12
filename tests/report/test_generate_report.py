import unittest

from app.report.datatypes import ErrorResponse
from app.report.generate import generate_report, get_orders_by_date


class TestGenerateReport(unittest.TestCase):
    def test_no_date(self):
        self.assertIsInstance(generate_report(None, None, None), ErrorResponse)
        self.assertIsInstance(generate_report("", "", ""), ErrorResponse)

    def test_invalid_date(self):
        self.assertIsInstance(
            generate_report(2020, 13, 1), ErrorResponse
        )  # invalid month
        self.assertIsInstance(
            generate_report(2020, 12, 40), ErrorResponse
        )  # invalid day


class TestGetOrdersByDate(unittest.TestCase):
    def test_no_date(self):
        self.assertEqual(get_orders_by_date(None), [])
