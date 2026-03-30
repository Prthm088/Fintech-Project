import time
import redis

from app.alerts.alert_queue import alert_queue
from app.notifications.telegram import send_telegram

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


def start_worker():

    while True:

        try:
            alert = alert_queue.get()

            print("WORKER RECEIVED ALERT:", alert)

            symbol = alert["symbol"]
            price = alert["price"]
            alert_type = alert["type"]

            # 🔥 Get all subscribers for this token
            redis_key = f"token_subscribers:{symbol}"
            chat_ids = r.smembers(redis_key)

            print(f"Sending to {len(chat_ids)} users")

            for chat_id in chat_ids:
                send_telegram(
                    chat_id,
                    symbol,
                    price,
                    alert_type
                )

        except Exception as e:
            print("Worker error:", e)

        time.sleep(0.5)