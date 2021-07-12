import unittest
from unittest.mock import Mock

from app.report.datatypes import ErrorResponse
from app.report.generate import (
    calc_num_customers,
    generate_report,
    get_orders_by_date,
)


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


class TestCalcNumCustomers(unittest.TestCase):
    def test_no_orders(self):
        self.assertEqual(calc_num_customers([]), 0)

    def test_none_orders(self):
        self.assertEqual(calc_num_customers(None), 0)

    def test_unique_customers(self):
        mock_orders = [Mock(customer_id=1), Mock(customer_id=2)]
        self.assertEqual(calc_num_customers(mock_orders), 2)

    def test_duplicated_customers(self):
        mock_orders = [
            Mock(customer_id=1),
            Mock(customer_id=1),
            Mock(customer_id=2),
        ]
        self.assertEqual(calc_num_customers(mock_orders), 2)
