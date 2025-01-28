from datetime import datetime, timedelta, timezone
import jwt
from config import JWT_ALGORITHM, JWT_EXPIRATION_SECONDS, JWT_SECRET

def encode_jwt(payload: dict) -> str | None:
    try:
        iat = datetime.now(timezone.utc)
        exp = iat + timedelta(seconds=JWT_EXPIRATION_SECONDS)

        payload.update({"exp": exp})
        payload.update({"iat": iat})

        print(f"JWT payload: {payload}")

        return jwt.encode(payload, JWT_SECRET.get_secret_value(), algorithm=JWT_ALGORITHM)
    except Exception as e:
        print(f"Error during JWT encoding: {e}")
        return None

def decode_jwt(token: str) -> dict | None:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        print("Invalid JWT token")
        return None
    except Exception as e:
        print(f"Error during JWT decoding: {e}")
        return None