from app.services import token_cache
from app.services.websocket_listener import sws

correlation_id = "fintech_project"
mode = 1


def refresh_subscriptions():

    print("Refreshing subscriptions...")

    token_cache.load_token_user_map()

    tokens = token_cache.subscribed_tokens

    print("Updated tokens:", tokens)

    if sws:

        token_list = [
            {
                "exchangeType": 1,
                "tokens": tokens
            }
        ]

        sws.subscribe(
            correlation_id,
            mode,
            token_list
        )

        print("WebSocket updated with new tokens")