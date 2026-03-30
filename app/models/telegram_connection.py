from app import db

class TelegramConnection(db.Model):
    __tablename__ = "telegram_connections"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    chat_id = db.Column(db.BigInteger, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())