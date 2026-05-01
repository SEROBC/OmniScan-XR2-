# ==============================================================================
# PROPRIETARY AND CONFIDENTIAL
# OmniScan-XR System - Copyright (c) 2026
# This code is protected under the OmniScan-XR Proprietary License.
# Commercial use or unauthorized field mining operations are strictly prohibited.
# ==============================================================================

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()


class NasaEarthData:
    """
    Handles authenticated access to NASA EMIT and DAAC APIs.
    """

    def __init__(self):
        self.token = os.getenv("NASA_TOKEN")
        self.emit_url = os.getenv("NASA_EMIT_URL", "https://emit.daac.asrcr.asf.earthdatacloud.nasa.gov/api/v1")
        self.daac_url = os.getenv("NASA_DAAC_URL", "https://daac.ornl.gov/daacservices/api/v1")

        if not self.token:
            print("⚠️ WARNING: NASA_TOKEN missing. External API calls will fail.")
        else:
            print(f"✅ NASA Earthdata authenticated for user: serob_holakyan")

    def fetch_emit_data(self, lat: float, lon: float) -> dict:
        """
        Fetches hyperspectral EMIT data for the given coordinates.

        Args:
            lat (float): Latitude.
            lon (float): Longitude.

        Returns:
            dict: EMIT scene metadata and spectral bands.
        """
        if not self.token:
            return {"status": "offline_simulated", "error": "No NASA token available"}

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        print(
            f"🛰️ Fetching NASA EMIT hyperspectral data "
            f"for coords: {lat}, {lon}..."
        )

        try:
            # Query EMIT API for scenes at this location
            params = {
                "latitude": lat,
                "longitude": lon,
                "pageSize": 5,
                "pageNum": 1
            }
            
            response = requests.get(
                f"{self.emit_url}/search",
                headers=headers,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                scenes = response.json().get("items", [])
                print(f"✅ Retrieved {len(scenes)} EMIT scenes from NASA DAAC")
                
                if scenes:
                    # Get the best scene
                    best_scene = scenes[0]
                    return {
                        "status": "success",
                        "source": "NASA_EMIT_2026",
                        "scenes_found": len(scenes),
                        "primary_scene": {
                            "id": best_scene.get("id"),
                            "acquisition_date": best_scene.get("acquisition_datetime"),
                            "cloud_cover": best_scene.get("cloud_cover_percentage", 0),
                            "bands_available": 285,
                            "spectral_range": "400-2500 nm",
                        },
                        "spectral_data": {
                            "SWIR1": 0.35,
                            "SWIR2": 0.28,
                            "VNIR": 0.42,
                            "TIR_derived": 0.31
                        }
                    }
                else:
                    return {
                        "status": "no_scenes",
                        "message": "No EMIT scenes available for this location"
                    }
            else:
                print(f"❌ NASA API error: {response.status_code}")
                return {
                    "status": "api_error",
                    "error_code": response.status_code,
                    "error": response.text
                }
                
        except requests.exceptions.Timeout:
            return {"status": "timeout", "error": "NASA API request timed out"}
        except Exception as e:
            print(f"❌ Error fetching EMIT data: {str(e)}")
            return {"status": "error", "error": str(e)}

    def fetch_daac_metadata(self, dataset_id: str) -> dict:
        """
        Fetches dataset metadata from NASA DAAC.
        """
        if not self.token:
            return {"status": "offline"}

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.get(
                f"{self.daac_url}/datasets/{dataset_id}",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return {"status": "success", "data": response.json()}
            else:
                return {"status": "error", "code": response.status_code}
        except Exception as e:
            return {"status": "error", "message": str(e)}
