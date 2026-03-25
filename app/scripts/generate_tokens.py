import pyotp
import os
from SmartApi import SmartConnect
from app.services.token_manager import save_tokens

# Load env (if using dotenv)
from dotenv import load_dotenv
load_dotenv()


def generate_tokens():
    client_id = os.getenv("ANGEL_CLIENT_ID")
    password = os.getenv("ANGEL_PASSWORD")
    totp_secret = os.getenv("ANGEL_TOTP_SECRET")

    # Step 1: Generate TOTP
    totp = pyotp.TOTP(totp_secret).now()

    try:
        # Step 2: Login
        smart_api = SmartConnect(api_key=client_id)

        session = smart_api.generateSession(client_id, password, totp)

        if not session["status"]:
            raise Exception(f"Login failed: {session}")

        auth_token = session["data"]["jwtToken"]

        # Step 3: Feed Token
        feed_token = smart_api.getfeedToken()

        # Step 4: Save to Redis
        save_tokens(auth_token, feed_token)

        print("Tokens generated and stored successfully")

    except Exception as e:
        print("Token generation failed:", str(e))


if __name__ == "__main__":
    generate_tokens()