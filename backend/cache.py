import redis
import json
from config import REDIS_HOST, REDIS_PORT

cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

def get_cache(key):
    data = cache.get(key)
    return json.loads(data) if data else None

def set_cache(key, value, ttl=3600):
    cache.setex(key, ttl, json.dumps(value))
