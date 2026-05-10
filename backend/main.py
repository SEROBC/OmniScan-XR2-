from fastapi import FastAPI
from routes import auth, scan, websocket

app = FastAPI()

app.include_router(auth.router)
app.include_router(scan.router)
app.include_router(websocket.router)

@app.get("/")
def root():
    return {"status": "XR2 MAX SYSTEM ONLINE"}
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
