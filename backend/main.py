from fastapi import FastAPI, Header, UploadFile, File, WebSocket
from pydantic import BaseModel
import uvicorn
import asyncio

from auth import create_token, verify_token
from nasa import fetch_emit
from detection import detect_objects
from websocket import stream

app = FastAPI()

# ===== MODELS =====
class AuthRequest(BaseModel):
    api_key: str

class ScanRequest(BaseModel):
    query: str
    lat: float = None
    lon: float = None


# ===== AUTH =====
@app.post("/auth")
def auth(data: AuthRequest):
    token = create_token(data.api_key)
    return {"token": token}


# ===== TEXT SCAN =====
@app.post("/scan")
async def scan(data: ScanRequest, authorization: str = Header(None)):
    verify_token(authorization)

    nasa_task = None
    if data.lat and data.lon:
        nasa_task = asyncio.to_thread(fetch_emit, data.lat, data.lon)

    # simple logic
    detected = "metal" in data.query.lower()

    nasa_data = await nasa_task if nasa_task else {}

    return {
        "detected": detected,
        "nasa": nasa_data
    }


# ===== IMAGE SCAN =====
@app.post("/scan-image")
async def scan_image(file: UploadFile = File(...), authorization: str = Header(None)):
    verify_token(authorization)

    contents = await file.read()

    import numpy as np
    import cv2

    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    detections = detect_objects(frame)

    return {"detections": detections}


# ===== WEBSOCKET =====
@app.websocket("/ws/stream")
async def ws_stream(ws: WebSocket):
    await stream(ws)


# ===== HEALTH =====
@app.get("/")
def root():
    return {"status": "XR2 PRODUCTION RUNNING"}


# ===== RUN =====
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
