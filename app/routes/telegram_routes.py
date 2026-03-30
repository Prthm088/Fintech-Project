from flask import Blueprint, request
from app import db
from app.models.telegram_connection import TelegramConnection
from app.services.token_redis import redis_client
from app.models.subscription import Subscription

telegram_bp = Blueprint("telegram", __name__)


@telegram_bp.route("/webhook", methods=["POST"])
def telegram_webhook():

    data = request.get_json()

    message = data.get("message")
    if not message:
        return "ok"

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text.startswith("/start"):
        parts = text.split()

        if len(parts) > 1:
            user_id = int(parts[1])

            existing = TelegramConnection.query.filter_by(chat_id=chat_id).first()

            if not existing:
                connection = TelegramConnection(
                    user_id=user_id,
                    chat_id=chat_id
                )
                db.session.add(connection)
                db.session.commit()

                print(f"✅ Saved: {user_id} → {chat_id}")

            # 🔥 NEW PART — REAL-TIME REDIS SYNC

            subs = Subscription.query.filter_by(user_id=user_id).all()

            for sub in subs:
                token = sub.stock.symbol   # or adjust based on your model

                redis_key = f"token_subscribers:{token}"
                redis_client.sadd(redis_key, chat_id)

                print(f"⚡ Added to Redis → {token} → {chat_id}")

    return "ok"