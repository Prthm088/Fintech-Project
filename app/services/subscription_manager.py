from app.services.token_redis import redis_client, load_token_user_map_to_redis
from app.services.websocket_listener import sws
from app.scripts.fetch_candle import get_orb_levels_for_tokens  # you create this

correlation_id = "fintech_project"
mode = 1

import json

def refresh_subscriptions():

    print("Refreshing subscriptions...")

    # ✅ 1. Check Redis connection
    try:
        redis_client.ping()
    except Exception as e:
        print(" Redis connection failed:", e)
        raise e

    # ✅ 2. Get old tokens
    old_tokens = set(map(str, redis_client.smembers("subscribed_tokens")))

    # ✅ 3. Reload from DB → Redis
    load_token_user_map_to_redis()

    # ✅ 4. Get updated tokens
    current_tokens = set(map(str, redis_client.smembers("subscribed_tokens")))

    print("Updated tokens:", current_tokens)

    if not current_tokens:
        print(" No tokens found after refresh")
        return

    # ✅ 5. Find new tokens
    new_tokens = current_tokens - old_tokens
    print("New tokens detected:", new_tokens)

    # ✅ 6. Remove stale ORB data (VERY IMPORTANT)
    for key in redis_client.scan_iter("orb_levels:*"):
        token = key.split(":")[1]
        if token not in current_tokens:
            redis_client.delete(key)

    # ✅ 7. Fetch ORB only for new tokens
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

    # ✅ 8. Update WebSocket subscription
    if sws:
        token_list = [
            {
                "exchangeType": 1,
                "tokens": list(map(int, current_tokens))  # 🔥 FIXED
            }
        ]

        sws.subscribe(correlation_id, mode, token_list)

        print("WebSocket updated with tokens")