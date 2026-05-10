import cv2
import base64
import asyncio
from fastapi import WebSocket
from detection import detect_objects

camera = cv2.VideoCapture(0)

async def stream(ws: WebSocket):
    await ws.accept()

    while True:
        success, frame = camera.read()
        if not success:
            continue

        detections = detect_objects(frame)

        _, buffer = cv2.imencode(".jpg", frame)
        frame_b64 = base64.b64encode(buffer).decode()

        await ws.send_json({
            "frame": frame_b64,
            "detections": detections
        })

        await asyncio.sleep(0.03)
