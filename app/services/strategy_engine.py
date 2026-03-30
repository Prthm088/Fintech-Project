import json
from app.services.token_redis import redis_client
from app.alerts.alert_queue import push_alert


def process_price_tick(token, price):

    token = str(token)

    # ✅ 1. Check if token is subscribed
    if not redis_client.sismember("subscribed_tokens", token):
        return

    # ✅ 2. Get ORB levels from Redis
    orb_data = redis_client.hgetall(f"orb_levels:{token}")

    if not orb_data:
        return

    high = float(orb_data["high"])
    low = float(orb_data["low"])

    # ✅ 3. Get trigger state from Redis
    trigger_data = redis_client.hgetall(f"triggered:{token}")

    breakout_triggered = trigger_data.get("breakout") == "1"
    breakdown_triggered = trigger_data.get("breakdown") == "1"

    # 🚀 BREAKOUT
    if price > high and not breakout_triggered:

        redis_client.hset(f"triggered:{token}", "breakout", 1)

        print(f"BREAKOUT detected for {token} at {price}")
        push_alert({
            "symbol": token,
            "price": price,
            "type": "breakout"
        })

    # 🚀 BREAKDOWN
    if price < low and not breakdown_triggered:

        redis_client.hset(f"triggered:{token}", "breakdown", 1)

        print(f"BREAKDOWN detected for {token} at {price}")

        push_alert({
            "symbol": token,
            "price": price,
            "type": "breakdown"
        })