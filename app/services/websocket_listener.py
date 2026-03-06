from app.services.strategy_engine import process_price_tick


def on_price_tick(data):

    token = data["token"]
    price = data["last_price"]

    process_price_tick(token, price)