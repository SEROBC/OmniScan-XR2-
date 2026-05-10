from fastapi import FastAPI
from routes import auth, scan, websocket

app = FastAPI()

app.include_router(auth.router)
app.include_router(scan.router)
app.include_router(websocket.router)

@app.get("/")
def root():
    return {"status": "XR2 MAX SYSTEM ONLINE"}        nasa_task = asyncio.to_thread(fetch_emit, data.lat, data.lon)

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
