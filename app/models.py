from . import db
from datetime import datetime

from datetime import datetime
from app import db

class Subscription(db.Model):
    __tablename__ = 'subscription'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    alert_type = db.Column(db.String(20), nullable=False)   # stock or ipo
    stock_name = db.Column(db.String(50), nullable=True)    # stock if alert_type = stock
    notification_method = db.Column(db.String(20), nullable=False)  # telegram/email/web
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # Relationship back to users table
    user = db.relationship("Users", backref="subscription")

    def __repr__(self):
        return f"<Subscription {self.id} - {self.alert_type}>"

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    password = db.Column(db.String(200),nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"<User {self.email}>"