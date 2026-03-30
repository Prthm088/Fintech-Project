import requests
import os
import logging
import time

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def send_telegram(chat_id, symbol, price, alert_type):
    """
    Sends Telegram alert safely with retries and error handling
    """

    message = format_message(symbol, price, alert_type)

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": chat_id,  # 🔥 dynamic now
        "text": message,
        "parse_mode": "Markdown"
    }

    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = requests.post(
                url,
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                logger.info(f"Telegram sent → chat_id={chat_id}")
                return True

            else:
                logger.warning(
                    f"Telegram failed (status {response.status_code}): {response.text}"
                )

        except requests.exceptions.RequestException as e:
            logger.error(f"Telegram request error: {e}")

        time.sleep(1)

    logger.error(f"Failed to send Telegram after retries → chat_id={chat_id}")
    return False


def format_message(symbol, price, alert_type):

    if alert_type == "breakout":
        emoji = "🚀"
        text = "BREAKOUT"
    else:
        emoji = "🔻"
        text = "BREAKDOWN"

    return (
        f"{emoji} *{symbol} {text}*\n"
        f"Price: `{price}`\n"
        f"Time: {time.strftime('%H:%M:%S')}"
    )