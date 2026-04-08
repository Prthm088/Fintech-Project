import json
import redis
import os
from app import db
from app.models import Subscription, Stock

# Redis connection on Development Server
# redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Redis connection on Production Server
REDIS_URL = os.environ.get("REDIS_URL")

# print("REDIS URL:", REDIS_URL)

redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5,
    retry_on_timeout=True
)

def load_token_user_map_to_redis():
    """
    Load all active subscriptions from DB → Redis
    """

    # 🔥 Clear old data (important)
    clear_token_data()

    results = (
        db.session.query(Subscription, Stock)
        .join(Stock, Subscription.stock_id == Stock.id)
        .filter(Subscription.is_active == True)
        .all()
    )

    for sub, stock in results:
        token = str(stock.token)

        user_data = {
            "user_id": sub.user_id,
            "symbol": stock.symbol,
            "method": sub.notification_method
        }

        # ✅ 1. Add user to token_users:{token}
        redis_client.rpush(f"token_users:{token}", json.dumps(user_data))

        # ✅ 2. Add token to subscribed_tokens set
        redis_client.sadd("subscribed_tokens", token)


def clear_token_data():
    """
    Clears old Redis token data
    """

    # Get all token keys
    keys = redis_client.keys("token_users:*")

    if keys:
        redis_client.delete(*keys)

    redis_client.delete("subscribed_tokens")