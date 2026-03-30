import json
from app.config.redis_client import redis_client

ORB_KEY = "orb_levels"


def set_orb_levels(levels):
    redis_client.set(ORB_KEY, json.dumps(levels))


def get_all_levels():
    data = redis_client.get(ORB_KEY)
    return json.loads(data) if data else {}


def get_level(token):
    data = redis_client.get(ORB_KEY)
    if not data:
        return None

    levels = json.loads(data)
    return levels.get(token)