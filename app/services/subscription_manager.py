from app.services.token_redis import redis_client, load_token_user_map_to_redis
from app.services.websocket_listener import sws
from app.scripts.fetch_candle import get_orb_levels_for_tokens  # you create this

correlation_id = "fintech_project"
mode = 1


def refresh_subscriptions():

    print("Refreshing subscriptions...")
    print("Testing Redis connection...")
    print(redis_client.ping())

    try:
        old_tokens = set(redis_client.smembers("subscribed_tokens"))
    except Exception as e:
        print("Redis error:", e)
        return  # 🔥 Prevent crash

    load_token_user_map_to_redis()

    try:
        current_tokens = set(redis_client.smembers("subscribed_tokens"))
    except Exception as e:
        print("Redis error:", e)
        return

    print("Updated tokens:", current_tokens)

    # ✅ 4. Find newly added tokens
    new_tokens = current_tokens - old_tokens

    print("New tokens detected:", new_tokens)

    # ✅ 5. Fetch ORB levels ONLY for new tokens
    if new_tokens:

        levels = get_orb_levels_for_tokens(list(new_tokens))

        for token, data in levels.items():
            redis_client.hset(
                f"orb_levels:{token}",
                mapping={
                    "high": data["high"],
                    "low": data["low"]
                }
            )

        print("ORB levels stored for new tokens")

    # ✅ 6. Update WebSocket subscription
    if sws and current_tokens:

        token_list = [
            {
                "exchangeType": 1,
                "tokens": list(current_tokens)
            }
        ]

        sws.subscribe(
            correlation_id,
            mode,
            token_list
        )

        print("WebSocket updated with new tokens")