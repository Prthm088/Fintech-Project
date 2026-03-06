from app import create_app
from app.services.token_cache import load_token_user_map
from app.services.strategy_engine import process_price_tick
from app.alerts.alert_worker import start_worker

import threading
import time

app = create_app()

# with app.app_context():
#     load_token_user_map()

# # start alert worker
# threading.Thread(target=start_worker, daemon=True).start()

# time.sleep(2)

# print("\n==============================")
# print("TESTING MULTIPLE PRICE TICKS")
# print("==============================\n")

# # first breakout tick
# process_price_tick("2885", 2501)

# time.sleep(1)

# # duplicate ticks
# process_price_tick("2885", 2502)
# process_price_tick("2885", 2503)
# process_price_tick("2885", 2504)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)