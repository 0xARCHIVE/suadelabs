from flask import Blueprint

from app.report.generate import generate_report

report_bp = Blueprint("report", __name__, url_prefix="/report")


@report_bp.route("/<int:year>/<int:month>/<int:day>")
def report_by_date(year: int, month: int, day: int) -> str:
    report = generate_report(year, month, day)
    return str(report)
