from datetime import datetime
from app import db

class Subscription(db.Model):
    __tablename__ = "subscriptions"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    alert_type = db.Column(db.String(20), nullable=False)  # stock / ipo

    stock_id = db.Column(
        db.Integer,
        db.ForeignKey("stocks.id"),
        nullable=False
    )

    notification_method = db.Column(
        db.String(20),
        nullable=False
    )  # telegram/email/web

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    is_active = db.Column(db.Boolean, default=True)

    user = db.relationship("Users", backref="subscriptions")
    stock = db.relationship("Stock", backref="subscriptions")

    def __repr__(self):
        return f"<Subscription {self.id} - {self.alert_type}>"