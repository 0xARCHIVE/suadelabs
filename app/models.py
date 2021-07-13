"""Database models.

These are the relevant tables from the CSV files provided in the coding test.
"""

from app.database import db


class Orders(db.Model):
    """Orders table (orders.csv)."""

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    vendor_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)

    orderlines = db.relationship("OrderLines", backref="order", lazy=True)


class OrderLines(db.Model):
    """OrderLines table (orderlines.csv)."""

    __tablename__ = "order_lines"

    order_id = db.Column(
        db.Integer, db.ForeignKey("orders.id"), primary_key=True
    )
    product_id = db.Column(db.Integer, primary_key=True)
    product_description = db.Column(db.Text, nullable=False)
    product_price = db.Column(db.Integer, nullable=False)
    product_vat_rate = db.Column(db.Float, nullable=False)
    discount_rate = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    full_price_amount = db.Column(db.Integer, nullable=False)
    discounted_amount = db.Column(db.Float, nullable=False)
    vat_amount = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)


class Commissions(db.Model):
    """Commissions table (commissions.csv)."""

    __tablename__ = "commissions"

    date = db.Column(db.Date, primary_key=True)
    vendor_id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Float, nullable=False)


class ProductPromotions(db.Model):
    """ProductPromotions table (product_promotions.csv)."""

    __tablename__ = "product_promotions"

    date = db.Column(db.Date, primary_key=True)
    product_id = db.Column(db.Integer, primary_key=True)
    promotion_id = db.Column(db.Integer)
