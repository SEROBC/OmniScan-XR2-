try:
    from ultralytics import YOLO
    model = YOLO("yolov8n.pt")
except:
    model = None

def detect(frame):
    if model is None:
        return [{"object": "mock", "confidence": 0.9}]

    results = model(frame)

    detections = []
    for r in results:
        for box in r.boxes:
            detections.append({
                "class": int(box.cls[0]),
                "confidence": float(box.conf[0])
            })

    return detections
