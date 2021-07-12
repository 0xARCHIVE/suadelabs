from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.report.routes import report_bp

app = Flask(__name__)
app.config.from_object("config")

db = SQLAlchemy(app)

app.register_blueprint(report_bp)
