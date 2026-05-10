from fastapi import APIRouter, WebSocket
import cv2, base64, asyncio
from services.detection_service import detect

router = APIRouter()

camera = cv2.VideoCapture(0)

@router.websocket("/ws")
async def ws(ws: WebSocket):
    await ws.accept()

    while True:
        ret, frame = camera.read()
        if not ret:
            continue

        detections = detect(frame)

        _, buffer = cv2.imencode(".jpg", frame)
        b64 = base64.b64encode(buffer).decode()

        await ws.send_json({
            "frame": b64,
            "detections": detections
        })

        await asyncio.sleep(0.03)
