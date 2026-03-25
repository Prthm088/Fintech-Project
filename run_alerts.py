from dotenv import load_dotenv
load_dotenv()

from app import create_app
from app.services.token_cache import load_token_user_map
from app.services.websocket_listener import start_websocket
from app.alerts.alert_worker import start_worker
from app.services.token_manager import get_auth_token

import threading
import time

app = create_app()


def start_system():
    with app.app_context():
        print("Loading token-user map...")
        load_token_user_map()

        # Critical: Ensure token exists before starting
        auth_token = get_auth_token()
        if not auth_token:
            raise Exception("No auth token found in Redis. Run token generator first.")

        print("Token found. Starting system...")

        # Start alert worker
        worker_thread = threading.Thread(target=start_worker, daemon=True)
        worker_thread.start()

        # Start websocket listener
        ws_thread = threading.Thread(target=start_websocket, daemon=True)
        ws_thread.start()

        # Keep process alive
        while True:
            time.sleep(5)


if __name__ == "__main__":
    start_system()