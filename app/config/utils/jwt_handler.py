from jose import JWTError, jwt
from datetime import datetime, timedelta

from app.config.env.data import JWT_ALGORITHM, JWT_EXPIRES_IN, JWT_SECRET


def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(days=JWT_EXPIRES_IN)

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError:
        return None
