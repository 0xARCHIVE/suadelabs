"""Module for generating a report (as specified by the coding test)."""

from datetime import date, timedelta
from typing import Dict, List, Tuple, Union

from app.models import Commissions, Orders, ProductPromotions
from app.report.datatypes import (
    CommissionReport,
    EmptyResponse,
    ErrorResponse,
    Report,
)


def get_orders_by_date(_date: date) -> List[Orders]:
    """Get a list of Orders placed on the given date."""
    if not _date:
        return []
    orders = Orders.query.filter(
        Orders.created_at >= _date,
        Orders.created_at <= _date + timedelta(days=1),
    ).all()
    return orders


def get_commission(_date: date, vendor_id: int) -> Commissions:
    """Get a Commissions object for a given date and vendor_id."""
    return Commissions.query.filter(
        Commissions.date == _date, Commissions.vendor_id == vendor_id
    ).first()


def get_promotion(_date: date, product_id: int) -> ProductPromotions:
    """Get a ProductPromotions object for a given date and product_id."""
    return ProductPromotions.query.filter(
        ProductPromotions.date == _date,
        ProductPromotions.product_id == product_id,
    ).first()


def calc_num_customers(orders: List[Orders]) -> int:
    """Calculate the number of unique customers from a list of Orders."""
    unique_customers = set()
    if not orders:
        return 0
    for order in orders:
        unique_customers.add(order.customer_id)
    return len(unique_customers)


def calc_discount_stats(orders: List[Orders]) -> Tuple[float, float]:
    """Calculate discount statistics from a list of Orders."""
    discount_amounts, discount_rates = ([], [])
    for order in orders:
        for orderline in order.orderlines:
            discount_amounts.append(orderline.discounted_amount)
            discount_rates.append(orderline.discount_rate)

    total_discount_amount = sum(discount_amounts)

    try:
        discount_rate_avg = sum(discount_rates) / len(discount_rates)
    except ZeroDivisionError:
        discount_rate_avg = 0.0

    return (total_discount_amount, discount_rate_avg)


def calc_order_total(order: Orders) -> float:
    """Calculate the total order amount for a given order."""
    order_total = 0.0

    if not order:
        return 0.0

    for orderline in order.orderlines:
        order_total += orderline.total_amount
    return order_total


def calc_order_stats(orders: List[Orders]) -> Tuple[int, float]:
    """Calculate order statistics from a list of Orders."""
    items, order_totals = ([], [])
    for order in orders:
        order_total = calc_order_total(order)
        order.total_amount = order_total
        order_totals.append(order_total)

        for orderline in order.orderlines:
            items.append(orderline.quantity)

    num_items = sum(items)
    try:
        order_total_avg = sum(order_totals) / len(order_totals)
    except ZeroDivisionError:
        order_total_avg = 0.0

    return (num_items, order_total_avg)


def calc_commission_stats(orders: List[Orders]) -> Tuple[float, float]:
    """Calculate commission statistics from a list of Orders."""
    commission_amounts = []
    for order in orders:
        _date = order.created_at.date()

        try:
            order_total = order.total_amount
        except AttributeError:
            order_total = calc_order_total(order)

        commission = get_commission(_date, order.vendor_id)
        commission_rate = commission.rate
        order_commission = order_total * commission_rate
        commission_amounts.append(order_commission)
    total_commission = sum(commission_amounts)

    try:
        order_average_commission = total_commission / len(commission_amounts)
    except ZeroDivisionError:
        order_average_commission = 0.0

    return (total_commission, order_average_commission)


def calc_promo_commissions(orders: List[Orders]) -> Dict[int, float]:
    """Calculate promotion commission statistics from a list of Orders."""
    promotions: Dict[int, float] = {}
    for order in orders:
        _date = order.created_at.date()
        commission = get_commission(_date, order.vendor_id)
        commission_rate = commission.rate

        for orderline in order.orderlines:
            promotion = get_promotion(_date, orderline.product_id)
            if promotion:
                promotion_id = int(promotion.promotion_id)
                commission_amount = commission_rate * orderline.total_amount
                try:
                    promotions[promotion_id] += commission_amount
                except KeyError:
                    promotions[promotion_id] = commission_amount
    return promotions


def generate_report(
    year: int, month: int, day: int
) -> Union[Report, ErrorResponse, EmptyResponse]:
    """Generate a Report object for the given date (year, month, day)."""
    try:
        _date = date(year, month, day)
    except (ValueError, TypeError):
        return ErrorResponse("Invalid date entered")

    orders = get_orders_by_date(_date)
    if not orders:
        return EmptyResponse()

    num_customers = calc_num_customers(orders)
    total_discount_amount, discount_rate_avg = calc_discount_stats(orders)
    num_items, order_total_avg = calc_order_stats(orders)

    total_commission, order_average_commission = calc_commission_stats(orders)
    promotion_commissions = calc_promo_commissions(orders)
    commissions = CommissionReport(
        promotion_commissions, total_commission, order_average_commission
    )

    report = Report(
        num_customers,
        total_discount_amount,
        num_items,
        order_total_avg,
        discount_rate_avg,
        commissions,
    )
    return report
