import secrets
import time
from fastapi import HTTPException
from config import API_KEY

TOKENS = {}

def create_token(api_key):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    token = secrets.token_hex(32)
    TOKENS[token] = {"created": time.time()}
    return token

def verify_token(token):
    if token not in TOKENS:
        raise HTTPException(status_code=401, detail="Unauthorized")
