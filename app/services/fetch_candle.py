from SmartApi import SmartConnect
import datetime
import os

from app.models.subscription import Subscription
from app import db

from services.orb_cache import set_orb_level


API_KEY = os.getenv("ANGEL_API_KEY")
AUTH_TOKEN = os.getenv("ANGEL_AUTH_TOKEN")

smartApi = SmartConnect(api_key=API_KEY)
smartApi.setAccessToken(AUTH_TOKEN)


def get_unique_tokens():

    subs = Subscription.query.with_entities(
        Subscription.symbol_token
    ).distinct().all()

    tokens = [s.symbol_token for s in subs]

    return tokens


def fetch_orb_for_token(token):

    today = datetime.date.today()

    historic_param = {
        "exchange": "NSE",
        "symboltoken": token,
        "interval": "FIFTEEN_MINUTE",
        "fromdate": f"{today} 09:15",
        "todate": f"{today} 09:30"
    }

    response = smartApi.getCandleData(historic_param)

    if not response["data"]:
        return

    candle = response["data"][0]

    high = candle[2]
    low = candle[3]

    set_orb_level(token, high, low)

    print(f"ORB set → {token} High:{high} Low:{low}")


def fetch_all_orb_levels():

    tokens = get_unique_tokens()

    print("Fetching ORB for tokens:", tokens)

    for token in tokens:
        fetch_orb_for_token(token)