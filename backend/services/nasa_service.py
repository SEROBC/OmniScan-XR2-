import requests
from core.config import NASA_TOKEN

def get_emit(lat, lon):
    try:
        res = requests.get(
            "https://emit.daac.asf.earthdatacloud.nasa.gov/api/v1/granules",
            headers={"Authorization": f"Bearer {NASA_TOKEN}"},
            params={"lat": lat, "lon": lon},
            timeout=10
        )
        return res.json()
    except:
        return {"error": "NASA unavailable"}
