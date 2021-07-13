"""app.report.generate testing suite."""

import unittest
from datetime import date, datetime
from unittest.mock import Mock, patch

from app.report.datatypes import CommissionReport, ErrorResponse, Report
from app.report.generate import (
    calc_commission_stats,
    calc_discount_stats,
    calc_num_customers,
    calc_order_stats,
    calc_order_total,
    calc_promo_commissions,
    generate_report,
    get_orders_by_date,
)


class TestGenerateReport(unittest.TestCase):
    """generate_report unit testing."""

    def test_no_date(self):
        """Input no date info (None or '')."""
        self.assertIsInstance(generate_report(None, None, None), ErrorResponse)
        self.assertIsInstance(generate_report("", "", ""), ErrorResponse)

    def test_invalid_date(self):
        """Input invalid dates."""
        self.assertIsInstance(
            generate_report(2020, 13, 1), ErrorResponse
        )  # invalid month
        self.assertIsInstance(
            generate_report(2020, 12, 40), ErrorResponse
        )  # invalid day

    @patch("app.report.generate.get_promotion")
    @patch("app.report.generate.get_commission")
    @patch("app.report.generate.get_orders_by_date")
    def test_with_data(
        self, mock_get_orders_by_date, mock_get_commission, mock_get_promotion
    ):
        """Check that a correct report is generated from mock data."""
        mock_order_data = {
            "id": 1,
            "created_at": datetime(2020, 1, 1, 23, 59, 59),
            "vendor_id": 1,
            "customer_id": 1,
        }

        mock_orderline_data = {
            "product_id": 1,
            "discount_rate": 0.1,
            "quantity": 10,
            "discounted_amount": 0.1,
            "total_amount": 1,
        }

        mock_commission_data = {
            "date": date(2020, 1, 1),
            "vendor_id": 1,
            "rate": 0.1,
        }

        mock_promo_data = {
            "date": date(2020, 1, 1),
            "product_id": 1,
            "promotion_id": 1,
        }

        mock_orderline = Mock(**mock_orderline_data)
        mock_order = Mock(**mock_order_data, orderlines=[mock_orderline])
        mock_get_orders_by_date.return_value = [mock_order]

        mock_get_commission.return_value = Mock(**mock_commission_data)
        mock_get_promotion.return_value = Mock(**mock_promo_data)

        expected_report = Report(
            customers=1,
            total_discount_amount=0.1,
            items=10,
            order_total_avg=1,
            discount_rate_avg=0.1,
            commissions=CommissionReport(
                promotions={1: 0.1}, total=0.1, order_average=0.1
            ),
        )

        self.assertEqual(generate_report(2020, 1, 1), expected_report)


class TestGetOrdersByDate(unittest.TestCase):
    """get_orders_by_date unit testing."""

    def test_no_date(self):
        """Input no date info."""
        self.assertEqual(get_orders_by_date(None), [])

    @patch(
        "flask_sqlalchemy._QueryProperty.__get__"
    )  # mocking Model.query is tricky (https://stackoverflow.com/a/42482171)
    def test_with_date(self, mock_query):
        """Check that an order is properly returned."""
        mock_order = Mock()
        mock_query.return_value.filter.return_value.all.return_value = [
            mock_order
        ]
        self.assertEqual(get_orders_by_date(date(2020, 1, 1)), [mock_order])


class TestCalcNumCustomers(unittest.TestCase):
    """calc_num_customers unit testing."""

    def test_no_orders(self):
        """Input no date info."""
        self.assertEqual(calc_num_customers([]), 0)

    def test_none_orders(self):
        """Input no orders."""
        self.assertEqual(calc_num_customers(None), 0)

    def test_unique_customers(self):
        """Check that unique customers are correctly counted."""
        mock_orders = [Mock(customer_id=1), Mock(customer_id=2)]
        self.assertEqual(calc_num_customers(mock_orders), 2)

    def test_duplicated_customers(self):
        """Check that duplicated customers are correctly counted."""
        mock_orders = [
            Mock(customer_id=1),
            Mock(customer_id=1),
            Mock(customer_id=2),
        ]
        self.assertEqual(calc_num_customers(mock_orders), 2)


class TestCalcDiscountStats(unittest.TestCase):
    """calc_discount_stats unit testing."""

    def test_no_orders(self):
        """Input no orders."""
        self.assertEqual(calc_discount_stats([]), (0.0, 0.0))

    def test_with_orders(self):
        """Check that statistics are correctly calculated."""
        mock_orderline = Mock(discounted_amount=1.0, discount_rate=0.1)
        mock_orders = [Mock(orderlines=[mock_orderline])]
        self.assertEqual(calc_discount_stats(mock_orders), (1.0, 0.1))


class TestCalcOrderTotal(unittest.TestCase):
    """calc_order_total unit testing."""

    def test_no_order(self):
        """Input no orders."""
        self.assertEqual(calc_order_total(None), 0.0)

    def test_with_order(self):
        """Check that order total is correctly calculated."""
        mock_orderline = Mock(total_amount=1.0)
        mock_order = Mock(orderlines=[mock_orderline])
        self.assertEqual(calc_order_total(mock_order), 1.0)


class TestCalcOrderStats(unittest.TestCase):
    """calc_order_stats unit testing."""

    def test_no_orders(self):
        """Input no orders."""
        self.assertEqual(calc_order_stats([]), (0, 0.0))

    @patch("app.report.generate.calc_order_total")
    def test_with_orders(self, mock_calc_order_total):
        """Check that order statistics are correctly calculacted."""
        mock_calc_order_total.return_value = 1.0
        mock_orderline = Mock(quantity=1)
        mock_orders = [Mock(orderlines=[mock_orderline])]

        self.assertEqual(calc_order_stats(mock_orders), (1, 1.0))


class TestCalcCommissionStats(unittest.TestCase):
    """calc_commission_stats unit testing."""

    def test_no_orders(self):
        """Input no orders."""
        self.assertEqual(calc_commission_stats([]), (0.0, 0.0))

    @patch("app.report.generate.get_commission")
    def test_with_orders_with_total_amount(self, mock_get_commission):
        """Check case where orders have 'total_amount' pre-calculated."""
        mock_order = Mock(created_at=datetime.now(), total_amount=1.0)
        mock_get_commission.return_value = Mock(rate=0.1)
        self.assertEqual(calc_commission_stats([mock_order]), (0.1, 0.1))

    @patch("app.report.generate.calc_order_total")
    @patch("app.report.generate.get_commission")
    def test_with_orders_no_total_amount(
        self, mock_get_commission, mock_calc_order_total
    ):
        """Check case where orders don't have 'total_amount' pre-calculated."""
        mock_order = Mock(created_at=datetime.now())
        del mock_order.total_amount

        mock_get_commission.return_value = Mock(rate=0.1)
        mock_calc_order_total.return_value = 1.0
        self.assertEqual(calc_commission_stats([mock_order]), (0.1, 0.1))


class TestCalcPromoCommissions(unittest.TestCase):
    """calc_promo_commissions unit testing."""

    def test_no_orders(self):
        """Input no orders."""
        self.assertEqual(calc_promo_commissions([]), {})

    @patch("app.report.generate.get_promotion")
    @patch("app.report.generate.get_commission")
    def test_with_orders(self, mock_get_commission, mock_get_promotion):
        """Check that promotion commissions are correctly calculated."""
        mock_orderline = Mock(total_amount=1.0)
        mock_order = Mock(
            created_at=datetime.now(), orderlines=[mock_orderline]
        )

        mock_get_commission.return_value = Mock(rate=0.1)
        mock_get_promotion.return_value = Mock(promotion_id=1)

        self.assertEqual(calc_promo_commissions([mock_order]), {1: 0.1})
