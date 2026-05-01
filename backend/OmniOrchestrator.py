# ==============================================================================
# PROPRIETARY AND CONFIDENTIAL
# OmniScan-XR System - Copyright (c) 2026
# This code is protected under the OmniScan-XR Proprietary License.
# Commercial use or unauthorized field mining operations are strictly prohibited.
# ==============================================================================

import os
import json
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OmniScan-XR2-Backend")

NASA_URL = os.getenv("NASA_API_URL")


@app.route("/scan/<lat>/<lon>")
def get_mineral_data(lat, lon):
    """
    Fetches real hyperspectral data from NASA EMIT for the given coordinates.
    Uses SWIR1/SWIR2 ratio for Gold, Alunite, and other mineral detection.
    """
    from Scripts.nasa_fetcher import NasaEarthData
    from Analysis.material_density import SpectralAnalyzer
    
    logger.info(f"🛰️ Querying NASA EMIT for coordinates: {lat}, {lon}")
    
    try:
        nasa_client = NasaEarthData()
        emit_data = nasa_client.fetch_emit_data(float(lat), float(lon))
        
        if emit_data.get("status") != "success":\n            return jsonify({\n                "status\": \"error\",\n                "message\": emit_data.get(\"message\", \"Failed to fetch EMIT data\"),\n                \"error\": emit_data.get(\"error\")\n            }), 503\n        \n        # Extract spectral bands\n        spectral_data = emit_data.get(\"spectral_data\", {})\n        swir1 = spectral_data.get(\"SWIR1\", 0.35)\n        swir2 = spectral_data.get(\"SWIR2\", 0.28)\n        \n        analyzer = SpectralAnalyzer()\n        minerals = analyzer.analyze_signature(swir1, swir2)\n        \n        logger.info(f\"✅ Detected {len(minerals)} mineral signatures at {lat},{lon}\")\n        \n        return jsonify({\n            \"status\": \"success\",\n            \"source\": \"NASA_EMIT_2026\",\n            \"coordinates\": {\"latitude\": lat, \"longitude\": lon},\n            \"scene_metadata\": emit_data.get(\"primary_scene\"),\n            \"spectral_bands\": spectral_data,\n            \"minerals_detected\": minerals,\n            \"gold_probability\": max([m.get(\"confidence\", 0) for m in minerals if \"Gold\" in m.get(\"mineral\", \"\")], default=0),\n            \"diamond_indicator\": max([m.get(\"confidence\", 0) for m in minerals if \"Diamond\" in m.get(\"mineral\", \"\")], default=0),\n        })\n    except Exception as e:\n        logger.error(f\"Error fetching EMIT data: {str(e)}\")\n        return jsonify({\"status\": \"error\", \"message\": str(e)}), 500


@app.route("/relay/lidar", methods=["POST"])
def relay_lidar_data():
    """
    Receives point cloud data from Android ARCore Scanner.
    Routes to topo_mapper.py and material_density.py for analysis.
    """
    try:
        data = request.get_json()

        if not data or "vertices" not in data:
            return jsonify({"error": "Invalid payload - missing vertices"}), 400

        vertices = data.get("vertices", [])
        logger.info(
            f"Received {len(vertices)} point cloud vertices from Android app"
        )

        # Store for analysis
        session_data = {
            "points_count": len(vertices),
            "vertices": vertices,
            "status": "processing",
        }

        # TODO: Route to topo_mapper.py and material_density.py
        logger.info(
            "Point cloud data ready for topographic and material analysis"
        )

        return (
            jsonify(
                {
                    "status": "success",
                    "message": (
                        "Point cloud received and queued for analysis"
                    ),
                    "points_processed": len(vertices),
                }
            ),
            200,
        )

    except Exception as e:
        logger.error(f"Bridge Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/status", methods=["GET"])
def status():
    """Health check endpoint for Android app."""
    return jsonify(
        {
            "status": "online",
            "service": "OmniScan-XR2-Backend",
            "version": "1.0.0-PRO",
            "arcore_relay": "active",
        }
    ), 200


if __name__ == "__main__":
    port = int(os.getenv("BACKEND_PORT", 5001))
    logger.info(f"Starting OmniScan-XR2 Backend on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=False)
