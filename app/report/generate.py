from datetime import date
from typing import List

from app.models import Orders
from app.report import Report


def get_orders_by_date(_date: date) -> List[Orders]:
    return []


def generate_report(year: int, month: int, day: int) -> Report:
    try:
        _date = date(year, month, day)
    except (ValueError, TypeError):
        return Report()

    return Report(_date)


#    orders = get_orders_by_date(_date)
