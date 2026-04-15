from flask import Blueprint, jsonify
from app.utils.health import system_health
from app.services.token_redis import redis_client

health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=["GET"])
def health():
    return jsonify(system_health())



@health_bp.route("/debug/redis", methods=["GET"])
def debug_redis():
    try:
        data = {}

        data["subscribed_tokens"] = list(redis_client.smembers("subscribed_tokens"))

        orb_data = {}
        for key in redis_client.scan_iter("orb_levels:*"):
            orb_data[key] = redis_client.hgetall(key)

        data["orb_levels"] = orb_data

        return jsonify({
            "status": "ok",
            "data": data
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })
    

@health_bp.route("/debug/subscriptions", methods=["GET"])
def debug_subscriptions():
    try:
        result = {}

        tokens = redis_client.smembers("subscribed_tokens")

        for token in tokens:
            result[token] = {
                "subscribers": list(redis_client.smembers(f"token_subscribers:{token}")),
                "orb": redis_client.hgetall(f"orb_levels:{token}"),
                "triggered": redis_client.hgetall(f"triggered:{token}")
            }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})