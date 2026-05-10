import cv2
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import torch

app = Flask(__name__)
CORS(app)

# =========================
# LOAD MODEL (YOLOv5 example)
# =========================
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

API_KEY = "XR2-SECURE-DEVICE-KEY"
TOKEN = "XR2-AUTH-TOKEN"

# =========================
# AUTH ROUTE (FIXED)
# =========================
@app.route("/auth", methods=["POST"])
def auth():
    data = request.json
    if data.get("api_key") == API_KEY:
        return jsonify({"token": TOKEN})
    return jsonify({"error": "Unauthorized"}), 401

# =========================
# DETECTION CORE
# =========================
def detect_objects(image):
    results = model(image)
    detections = []

    for *box, conf, cls in results.xyxy[0]:
        detections.append({
            "label": model.names[int(cls)],
            "confidence": float(conf),
            "box": [float(x) for x in box]
        })

    return detections

# =========================
# SCAN ROUTE
# =========================
@app.route("/scan", methods=["POST"])
def scan():
    token = request.headers.get("Authorization")

    if token != TOKEN:
        return jsonify({"error": "Invalid token"}), 403

    file = request.files.get("image")

    if not file:
        return jsonify({"error": "No image provided"}), 400

    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    detections = detect_objects(img)

    return jsonify({
        "detections": detections,
        "count": len(detections)
    })

# =========================
# LIVE CAMERA STREAM
# =========================
@app.route("/live", methods=["GET"])
def live():
    cap = cv2.VideoCapture(0)

    results_data = []

    ret, frame = cap.read()
    if ret:
        detections = detect_objects(frame)
        results_data = detections

    cap.release()

    return jsonify({
        "live_detections": results_data
    })

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
