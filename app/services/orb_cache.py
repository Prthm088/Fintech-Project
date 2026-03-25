# services/orb_cache.py

ORB_LEVELS = {}

def set_orb_level(token, high, low):
    ORB_LEVELS[token] = {
        "high": high,
        "low": low
    }

def get_orb_level(token):
    return ORB_LEVELS.get(token)

def get_all_levels():
    return ORB_LEVELS