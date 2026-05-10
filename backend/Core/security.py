from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY = "XR2_SECRET"
ALGORITHM = "HS256"

def create_token(data: dict, expires=60):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=expires)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
