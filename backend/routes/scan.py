from fastapi import APIRouter, UploadFile, File, Header
import numpy as np
import cv2

from core.security import verify_token
from services.detection_service import detect
from services.nasa_service import get_emit

router = APIRouter()

@router.post("/scan-image")
async def scan_image(file: UploadFile = File(...), authorization: str = Header(None)):
    user = verify_token(authorization)
    if not user:
        return {"error": "Unauthorized"}

    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    detections = detect(frame)

    return {"detections": detections}


@router.get("/scan/{lat}/{lon}")
def scan_geo(lat: float, lon: float, authorization: str = Header(None)):
    if not verify_token(authorization):
        return {"error": "Unauthorized"}

    nasa = get_emit(lat, lon)

    return {"nasa": nasa}
