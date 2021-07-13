"""Reporting routes, /report/xxx."""

from dataclasses import asdict
from typing import Any, Dict

from flask import Blueprint

from app.report.generate import generate_report

report_blueprint = Blueprint("report", __name__, url_prefix="/report")


@report_blueprint.route("/<int:year>/<int:month>/<int:day>")
def report_by_date(year: int, month: int, day: int) -> Dict[Any, Any]:
    """Return a report for the given date yyyy/mm/dd."""
    report = generate_report(year, month, day)
    return asdict(report)
