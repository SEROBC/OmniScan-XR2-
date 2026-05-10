import os
from dotenv import load_dotenv

load_dotenv()

NASA_TOKEN = os.getenv("NASA_TOKEN")
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
