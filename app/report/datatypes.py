"""Datatypes.

The reports keep data logically grouped and type-checked. They get
converted to a dict and sent out through the /report endpoint.

The extra response types are also for use with the endpoint, and allow
custom messages to be sent (e.g. error info).
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class CommissionReport:
    """Commission sub-report."""

    promotions: Dict[int, float]
    total: float
    order_average: float


@dataclass
class Report:
    """The main report that is populated and displayed."""

    customers: int
    total_discount_amount: float
    items: int
    order_total_avg: float
    discount_rate_avg: float
    commissions: CommissionReport


@dataclass
class ErrorResponse:
    """A response for providing useful error messages to the user."""

    error: str


@dataclass
class EmptyResponse:
    """An empty response."""

    pass
