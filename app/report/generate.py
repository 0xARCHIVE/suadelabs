from datetime import date, timedelta
from typing import Dict, List, Tuple, Union

from app.models import Orders
from app.report.datatypes import CommissionReport, ErrorResponse, Report


def calc_num_customers(orders: List[Orders]) -> int:
    unique_customers = set()
    if not orders:
        return 0
    for order in orders:
        unique_customers.add(order.customer_id)
    return len(unique_customers)


def calc_discount_stats(orders: List[Orders]) -> Tuple[float, float]:
    raise NotImplementedError


def calc_order_stats(orders: List[Orders]) -> Tuple[int, float]:
    raise NotImplementedError


def calc_commission_stats(orders: List[Orders]) -> Tuple[float, float]:
    raise NotImplementedError


def calc_promo_commissions(orders: List[Orders]) -> Dict[str, float]:
    raise NotImplementedError


def get_orders_by_date(_date: date) -> List[Orders]:
    if not _date:
        return []
    orders = Orders.query.filter(
        Orders.created_at >= _date,
        Orders.created_at <= _date + timedelta(days=1),
    ).all()
    return orders


def generate_report(
    year: int, month: int, day: int
) -> Union[Report, ErrorResponse]:
    try:
        _date = date(year, month, day)
    except (ValueError, TypeError):
        return ErrorResponse("Invalid date entered")

    orders = get_orders_by_date(_date)

    num_customers = calc_num_customers(orders)
    total_discount_amount, discount_rate_avg = calc_discount_stats(orders)
    num_items, order_total_avg = calc_order_stats(orders)

    promotion_commissions = calc_promo_commissions(orders)
    total_commission, order_average_commission = calc_commission_stats(orders)
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
