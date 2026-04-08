from app import create_app
from app.models.telegram_connection import TelegramConnection
from app.models.subscription import Subscription  # your existing model
import redis
import os

app = create_app()

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


from app.models.stock import Stock

def sync_telegram_to_redis():
    with app.app_context():

        # Clear old data
        for key in r.keys("token_subscribers:*"):
            r.delete(key)

        connections = TelegramConnection.query.all()

        for conn in connections:
            user_id = conn.user_id
            chat_id = conn.chat_id

            subs = Subscription.query.filter_by(user_id=user_id).all()

            for sub in subs:
                # ✅ FIX
                stock = Stock.query.get(sub.stock_id)

                if not stock:
                    continue  # safety

                token = stock.token  # or stock.token

                redis_key = f"token_subscribers:{token}"
                r.sadd(redis_key, chat_id)

        print("Telegram subscribers synced to Redis")