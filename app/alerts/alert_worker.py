import time

from app.alerts.alert_queue import alert_queue
from app.notifications.telegram import send_telegram


def start_worker():

    # print("Alert worker started")

    while True:

        try:

            alert = alert_queue.get()

            print("WORKER RECEIVED ALERT:", alert)

            send_telegram(
                alert["user_id"],
                alert["symbol"],
                alert["price"],
                alert["type"]
            )

        except Exception as e:

            print("Worker error:", e)

        time.sleep(0.5)