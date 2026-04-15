import os
from app.services.token_redis import redis_client


def check_redis():
    try:
        redis_client.ping()
        return True, "Redis OK"
    except Exception as e:
        return False, str(e)


def check_env():
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        return False, "REDIS_URL missing"
    return True, "ENV OK"


def system_health():
    health = {}

    redis_ok, redis_msg = check_redis()
    env_ok, env_msg = check_env()

    health["redis"] = {"status": redis_ok, "message": redis_msg}
    health["env"] = {"status": env_ok, "message": env_msg}

    overall = redis_ok and env_ok

    return {
        "overall": overall,
        "checks": health
    }