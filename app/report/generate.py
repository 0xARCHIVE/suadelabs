from datetime import date, timedelta
from typing import List, Union

from app.models import Orders
from app.report.datatypes import ErrorResponse, Report


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

    get_orders_by_date(_date)
    return ErrorResponse("Not yet implemented")


#    orders = get_orders_by_date(_date)
