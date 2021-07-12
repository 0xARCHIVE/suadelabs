from dataclasses import dataclass
from typing import Dict


@dataclass
class CommissionReport:
    promotions: Dict[str, float]
    total: float
    order_average: float


@dataclass
class Report:
    customers: int
    total_discount_amount: float
    items: int
    order_total_avg: float
    discount_rate_avg: float
    commissions: CommissionReport


@dataclass
class ErrorResponse:
    error: str
