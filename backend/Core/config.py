import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret")
API_KEY = os.getenv("API_KEY")
NASA_TOKEN = os.getenv("NASA_TOKEN")

DB_URL = os.getenv("DB_URL", "sqlite:///./xr2.db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
