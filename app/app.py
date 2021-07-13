"""Main app entrypoint."""

from flask import Flask

from app.database import db
from app.report.routes import report_blueprint


def create_app() -> Flask:
    """Create Flask app."""
    app = Flask(__name__)
    app.config.from_object("config")
    db.init_app(app)
    app.register_blueprint(report_blueprint)
    return app
