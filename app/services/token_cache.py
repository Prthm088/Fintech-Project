from app import db
from app.models import Subscription, Stock

token_user_map = {}

def load_token_user_map():

    global token_user_map
    token_user_map = {}

    results = (
        db.session.query(Subscription, Stock)
        .join(Stock, Subscription.stock_id == Stock.id)
        .filter(Subscription.is_active == True)
        .all()
    )

    for sub, stock in results:

        token = stock.token

        if token not in token_user_map:
            token_user_map[token] = []

        token_user_map[token].append({
            "user_id": sub.user_id,
            "symbol": stock.symbol,
            "method": sub.notification_method
        })

    print("\nTOKEN USER CACHE:")
    print(token_user_map)