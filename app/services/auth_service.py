from SmartApi import SmartConnect
import pyotp
import os


def generate_feed_token():

    api_key = os.getenv("ANGEL_API_KEY")
    client_code = os.getenv("ANGEL_CLIENT_CODE")
    password = os.getenv("ANGEL_PASSWORD")
    totp_secret = os.getenv("ANGEL_TOTP_SECRET")

    smart_api = SmartConnect(api_key)

    totp = pyotp.TOTP(totp_secret).now()

    data = smart_api.generateSession(client_code, password, totp)

    feed_token = smart_api.getfeedToken()

    return feed_token