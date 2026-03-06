from app.services import token_cache
from app.alerts.alert_queue import push_alert

# FOR TESTING
orb_levels = {
    "2885": {
        "high": 2500,
        "low": 2480
    }
}

# ORB levels
# orb_levels = {}

# Trigger memory
triggered_alerts = {}


def set_orb_levels(levels):

    global orb_levels
    orb_levels = levels


def process_price_tick(token, price):

    if token not in orb_levels:
        return

    high = orb_levels[token]["high"]
    low = orb_levels[token]["low"]

    # initialize trigger memory
    if token not in triggered_alerts:
        triggered_alerts[token] = {
            "breakout": False,
            "breakdown": False
        }

    users = token_cache.token_user_map.get(token, [])

    # BREAKOUT
    if price > high and not triggered_alerts[token]["breakout"]:

        triggered_alerts[token]["breakout"] = True

        print(f"BREAKOUT detected for {token} at {price}")

        users = token_cache.token_user_map.get(token, [])
        print("USERS TO ALERT:", users)

        for user in users:

            alert = {
                "user_id": user["user_id"],
                "symbol": user["symbol"],
                "price": price,
                "type": "breakout",
                "method": user["method"]
            }

            print("SENDING ALERT TO QUEUE:", alert)

            push_alert(alert)
    # BREAKDOWN
    if price < low and not triggered_alerts[token]["breakdown"]:

        triggered_alerts[token]["breakdown"] = True

        print(f"BREAKDOWN detected for {token} at {price}")
        print("Current Trigger Memory:", triggered_alerts)
        for user in users:

            push_alert({
                "user_id": user["user_id"],
                "symbol": user["symbol"],
                "price": price,
                "type": "breakdown",
                "method": user["method"]
            })

