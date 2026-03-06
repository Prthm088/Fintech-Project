import requests

BOT_TOKEN = "YOUR_TOKEN"


def send_telegram(user_id, symbol, price, alert_type):

    # message = f"{symbol} BREAKOUT at {price}"

    # url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    # requests.post(url, json={
    #     "chat_id": user_id,
    #     "text": message
    # })

    ## FOR TESTING
    print("\n===== TELEGRAM ALERT =====")
    print("User:", user_id)
    print("Stock:", symbol)
    print("Price:", price)
    print("Type:", alert_type)
    print("==========================\n")
