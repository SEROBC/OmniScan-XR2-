import hashlib
import hmac

SECRET = b"XR2_SECURE"

def sign(data: bytes):
    return hmac.new(SECRET, data, hashlib.sha256).hexdigest()

def verify(data: bytes, signature: str):
    return sign(data) == signature
