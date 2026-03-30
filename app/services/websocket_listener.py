sws = None
import os
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from logzero import logger

from app.services.strategy_engine import process_price_tick
from app.services import token_redis
from app.services.token_manager import get_auth_token,get_feed_token

API_KEY = os.environ.get("ANGEL_API_KEY")
CLIENT_CODE = os.environ.get("ANGEL_CLIENT_CODE")

correlation_id = "fintech_project"
mode = 1  # LTP


from app.services.token_redis import redis_client

def start_websocket():

    global sws

    AUTH_TOKEN = get_auth_token()
    FEED_TOKEN = get_feed_token()

    tokens = list(map(str, redis_client.smembers("subscribed_tokens")))

    logger.info(f"Subscribing to tokens: {tokens}")

    token_list = [
        {
            "exchangeType": 1,
            "tokens": tokens
        }
    ]

    sws = SmartWebSocketV2(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN)

    def on_data(wsapp, message):

        try:
            if "last_traded_price" in message:

                token = str(message["token"])
                price = float(message["last_traded_price"]) * 0.01
                # print(f"TICK token={token} price={price}")
                process_price_tick(token, price)

        except Exception as e:
            logger.error(f"Tick processing error: {e}")

    def on_open(wsapp):
        logger.info("WebSocket connected")
        sws.subscribe(correlation_id, mode, token_list)

    def on_close(wsapp):
        logger.warning("WebSocket closed. Reconnecting...")
        start_websocket()

    sws.on_open = on_open
    sws.on_data = on_data
    sws.on_error = lambda ws, err: logger.error(f"Error: {err}")
    sws.on_close = on_close

    sws.connect()