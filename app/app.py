from flask import Flask

from app.database import db
from app.report.routes import report_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config")
    db.init_app(app)
    app.register_blueprint(report_bp)
    return app
