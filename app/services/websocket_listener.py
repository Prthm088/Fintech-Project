sws = None
import os
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from logzero import logger

from app.services.strategy_engine import process_price_tick
from app.services import token_cache


AUTH_TOKEN = os.environ.get("ANGEL_AUTH_TOKEN")
API_KEY = os.environ.get("ANGEL_API_KEY")
CLIENT_CODE = os.environ.get("ANGEL_CLIENT_CODE")
FEED_TOKEN = os.environ.get("ANGEL_FEED_TOKEN")

correlation_id = "fintech_project"
mode = 1  # LTP


def start_websocket():

    global sws

    tokens = token_cache.subscribed_tokens

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

                logger.info(f"TICK   token={token} price={price}")

                # Send tick to strategy engine
                process_price_tick(token, price)

        except Exception as e:

            logger.error(f"Tick processing error: {e}")

    def on_open(wsapp):

        logger.info("WebSocket connected")

        sws.subscribe(
            correlation_id,
            mode,
            token_list
        )
        # TEST TICK (for closed market testing)
        # from app.services.strategy_engine import process_price_tick

        # process_price_tick("2885", 2505)

    def on_error(wsapp, error):

        logger.error(f"WebSocket error: {error}")

    def on_close(wsapp):

        logger.info("WebSocket closed")

    sws.on_open = on_open
    sws.on_data = on_data
    sws.on_error = on_error
    sws.on_close = on_close

    sws.connect()