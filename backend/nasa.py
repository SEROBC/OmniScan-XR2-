import requests
from config import NASA_TOKEN
from cache import get_cache, set_cache

BASE_URL = "https://emit.daac.asrcr.asf.earthdatacloud.nasa.gov/api/v1"

def fetch_emit(lat, lon):
    key = f"emit:{lat}:{lon}"
    cached = get_cache(key)
    if cached:
        return cached

    headers = {"Authorization": f"Bearer {NASA_TOKEN}"}

    try:
        res = requests.get(
            f"{BASE_URL}/granules",
            params={"lat": lat, "lon": lon},
            headers=headers,
            timeout=10
        )

        data = res.json()
        set_cache(key, data)

        return data

    except Exception:
        return {"error": "NASA unavailable"}
