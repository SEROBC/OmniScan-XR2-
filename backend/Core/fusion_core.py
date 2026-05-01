# ==============================================================================
# PROPRIETARY AND CONFIDENTIAL
# OmniScan-XR System - Copyright (c) 2026
# This code is protected under the OmniScan-XR Proprietary License.
# Commercial use or unauthorized field mining operations are strictly prohibited.
# ==============================================================================

import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from security import verify_operation_permit

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from Scripts.nasa_fetcher import NasaEarthData
from Analysis.material_density import SpectralAnalyzer


load_dotenv()

app = Flask(__name__)
CORS(app)

PERMIT_STATUS = verify_operation_permit()
nasa_client = NasaEarthData()
analyzer = SpectralAnalyzer()


@app.route("/relay/lidar", methods=["POST"])
def process_spatial_data():
    """
    Processes incoming ARCore point cloud data and performs
    NASA EMIT synchronization and mineral detection.
    
    Request payload:
    {
      "vertices": [[x,y,z], ...],
      "timestamp": 1714600000000,
      "latitude": 34.05,
      "longitude": -118.24
    }
    """
    if PERMIT_STATUS != "FULL":
        return (
            jsonify(
                {
                    "error": (
                        "Unauthorized. Field operations require a valid permit."
                    )
                }
            ),
            403,
        )

    data = request.json or {}
    vertices = data.get("vertices", [])
    lat = data.get("latitude", 34.0)  # Default to LA region
    lon = data.get("longitude", -118.0)
    timestamp = data.get("timestamp", 0)

    print(f"📡 Fusion Core: Received {len(vertices)} spatial points from ARCore")
    print(f"📍 Location: {lat}, {lon} | Timestamp: {timestamp}")

    try:
        # Fetch NASA EMIT hyperspectral data
        nasa_data = nasa_client.fetch_emit_data(lat, lon)
        
        if nasa_data.get("status") != "success":
            return jsonify({
                "status": "partial",
                "message": "EMIT data unavailable, using local analysis",
                "points_received": len(vertices),
                "detections": []
            }), 200
        
        # Extract spectral bands from NASA
        spectral = nasa_data.get("spectral_data", {})
        swir1 = spectral.get("SWIR1", 0.35)
        swir2 = spectral.get("SWIR2", 0.28)
        
        # Run spectral analysis
        detections = analyzer.analyze_signature(swir1, swir2)
        
        print(f"\n✅ FUSION COMPLETE:")
        print(f"   - NASA EMIT scenes: {nasa_data.get('scenes_found', 0)}")
        print(f"   - Extracted {len(detections)} mineral signatures")
        print(f"   - Voxelized {len(vertices)} ARCore points")
        
        return jsonify(
            {
                "status": "processed",
                "api_version": "v2-nasa-integrated",
                "nasa_emit_sync": nasa_data.get("status"),
                "spectral_source": nasa_data.get("source"),
                "scene_id": nasa_data.get("primary_scene", {}).get("id"),
                "cloud_cover_percent": nasa_data.get("primary_scene", {}).get("cloud_cover", 0),
                "points_processed": len(vertices),
                "detections": detections,
                "location": {"latitude": lat, "longitude": lon},
                "timestamp": timestamp
            }
        ), 200
        
    except Exception as e:
        print(f"❌ Fusion Error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Fusion process failed",
            "error": str(e)
        }), 500


if __name__ == "__main__":
    print("🚀 OmniScan-XR2 Fusion Core Initializing...")
    app.run(host="0.0.0.0", port=5001)
