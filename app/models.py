from . import db

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_name = db.Column(db.String(100), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)
