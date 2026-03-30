from dotenv import load_dotenv
load_dotenv()

from SmartApi import SmartConnect
from datetime import datetime, time
import pyotp
import os
import time as time_module

from app.config.redis_client import redis_client


# 🔑 ENV
API_KEY = os.getenv("HISTORICAL_CLIENT_ID")
CLIENT_ID = os.getenv("ANGEL_CLIENT_ID")
PASSWORD = os.getenv("ANGEL_PASSWORD")
TOTP_SECRET = os.getenv("ANGEL_TOTP_SECRET")


# 📅 Helper
def get_today_date():
    
    return datetime.now().strftime("%Y-%m-%d")


# 🔥 1. FETCH ORB LEVELS (NO REDIS HERE)
def fetch_orb_levels(tokens):

    # ⛔ Safety check
    if datetime.now().time() < time(9, 30):
        print("ORB not ready yet, skipping...")
        return {}

    # 🔑 Generate TOTP
    totp = pyotp.TOTP(TOTP_SECRET).now()

    # 🔌 Login ONCE
    smart_api = SmartConnect(api_key=API_KEY)
    session = smart_api.generateSession(CLIENT_ID, PASSWORD, totp)

    if not session["status"]:
        raise Exception(f"Login failed: {session}")

    print("Logged in for historical data")

    today = get_today_date()
    from_time = f"{today} 09:15"
    to_time = f"{today} 09:30"

    orb_data = {}

    for token in tokens:
        try:
            params = {
                "exchange": "NSE",
                "symboltoken": token,
                "interval": "FIFTEEN_MINUTE",
                "fromdate": from_time,
                "todate": to_time
            }

            response = smart_api.getCandleData(params)

            if not response.get("status") or not response.get("data"):
                print(f"No data for token {token}")
                continue

            candle = response["data"][0]

            high = float(candle[2])
            low = float(candle[3])

            orb_data[token] = {
                "high": high,
                "low": low
            }

            print(f"ORB → token={token} high={high} low={low}")

        except Exception as e:
            print(f"Error for token {token}: {e}")

        # ⚠️ Rate limit protection
        time_module.sleep(0.4)

    return orb_data


# 🔥 2. STORE IN REDIS (PER TOKEN)
def store_orb_levels_in_redis(levels):

    for token, data in levels.items():
        redis_client.hset(
            f"orb_levels:{token}",
            mapping={
                "high": data["high"],
                "low": data["low"]
            }
        )

    print("ORB levels stored in Redis")


# 🔥 3. FETCH + STORE (USED AT STARTUP OR SCHEDULE)
def load_orb_levels(tokens):

    levels = fetch_orb_levels(tokens)

    store_orb_levels_in_redis(levels)

    return levels


# 🔥 4. FETCH ONLY FOR NEW TOKENS (USED IN SUBSCRIPTION MANAGER)
def get_orb_levels_for_tokens(tokens):

    if not tokens:
        return {}

    levels = fetch_orb_levels(tokens)

    return levels


# 🔥 OPTIONAL: GET FROM REDIS (DEBUG / TEST)
def get_orb_from_redis(token):

    data = redis_client.hgetall(f"orb_levels:{token}")

    if not data:
        return None

    return {
        "high": float(data["high"]),
        "low": float(data["low"])
    }


# 🔥 TEST
if __name__ == "__main__":

    tokens = ["2885", "4963"]

    levels = load_orb_levels(tokens)

    print("FINAL LEVELS:", levels)


## For testing use this 

# from app.config.redis_client import redis_client

# # Mock ORB levels
# redis_client.hset("orb_levels:2885", mapping={
#     "high": 2500,
#     "low": 2480
# })

# redis_client.hset("orb_levels:4963", mapping={
#     "high": 1000,
#     "low": 980
# })

# print("Mock ORB levels inserted")