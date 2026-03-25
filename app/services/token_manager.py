import json
from app.config.redis_client import redis_client

TOKEN_KEY = "angel_tokens"


def save_tokens(auth_token, feed_token):
    data = {
        "auth_token": auth_token,
        "feed_token": feed_token
    }
    redis_client.set(TOKEN_KEY, json.dumps(data))


def get_tokens():
    data = redis_client.get(TOKEN_KEY)
    if not data:
        return None

    return json.loads(data)


def get_auth_token():
    tokens = get_tokens()
    return tokens["auth_token"] if tokens else None


def get_feed_token():
    tokens = get_tokens()
    return tokens["feed_token"] if tokens else None