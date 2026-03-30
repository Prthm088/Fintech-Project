import requests
import time
import os

from app import create_app, db
from app.models.telegram_connection import TelegramConnection

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

app = create_app()

last_update_id = None


def handle_update(update):
    global last_update_id

    message = update.get("message")
    if not message:
        return

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text.startswith("/start"):
        parts = text.split()

        if len(parts) > 1:
            user_id = int(parts[1])

            with app.app_context():

                # 🔍 Check if chat already exists
                existing = TelegramConnection.query.filter_by(chat_id=chat_id).first()

                if existing:
                    print(f"⚠️ Chat already linked: {chat_id}")
                    return

                # 🔥 Save mapping
                connection = TelegramConnection(
                    user_id=user_id,
                    chat_id=chat_id
                )

                db.session.add(connection)
                db.session.commit()

                print(f"✅ Saved: user_id={user_id} → chat_id={chat_id}")


def get_updates():
    global last_update_id

    url = f"{BASE_URL}/getUpdates"

    params = {}
    if last_update_id:
        params["offset"] = last_update_id + 1

    response = requests.get(url, params=params).json()

    for update in response["result"]:
        last_update_id = update["update_id"]
        handle_update(update)


if __name__ == "__main__":
    while True:
        get_updates()
        time.sleep(2)