# ==============================================================================
# PROPRIETARY AND CONFIDENTIAL
# OmniScan-XR System - Copyright (c) 2026 Serob Cholakyan
# This code is protected under the OmniScan-XR Proprietary License.
# ==============================================================================

"""
NASA EMIT & DAAC API Configuration

This module manages all NASA satellite data endpoints and authentication.
Token: serob_holakyan (Valid until: 2026-05-18)
"""

import os
from dotenv import load_dotenv

load_dotenv()

class NASAConfig:
    """NASA API endpoint configuration and authentication manager."""
    
    # Authentication
    TOKEN = os.getenv("NASA_TOKEN")
    
    # EMIT (Earth Surface Mineral Dust Source Investigation)
    EMIT_API_BASE = os.getenv(
        "NASA_EMIT_URL",
        "https://emit.daac.asrcr.asf.earthdatacloud.nasa.gov/api/v1"
    )
    EMIT_SEARCH = f"{EMIT_API_BASE}/search"
    EMIT_GRANULES = f"{EMIT_API_BASE}/granules"
    EMIT_QUICKLOOKS = f"{EMIT_API_BASE}/granules/{{id}}/quicklook"
    
    # LP DAAC (Land Processes Distributed Active Archive Center)
    LPDAAC_BASE = "https://lpdaacsvc.cr.usgs.gov/services/inventory"
    LPDAAC_LP_DAAC = f"{LPDAAC_BASE}/lp-daac"
    
    # DAAC General Access
    DAAC_API_BASE = os.getenv(
        "NASA_DAAC_URL",
        "https://daac.ornl.gov/daacservices/api/v1"
    )
    DAAC_DATASETS = f"{DAAC_API_BASE}/datasets"
    DAAC_SEARCH = f"{DAAC_API_BASE}/datasets/search"
    
    # ASF DAAC (Alaska Satellite Facility)
    ASF_CMRGY_BASE = "https://cmr.earthdata.nasa.gov/search"
    ASF_CMR_COLLECTIONS = f"{ASF_CMRGY_BASE}/collections"
    ASF_CMR_GRANULES = f"{ASF_CMRGY_BASE}/granules"
    
    # Earthdata Search
    EARTHDATA_SEARCH = "https://search.earthdata.nasa.gov"
    
    # CMR (Common Metadata Repository) - Central Discovery
    CMR_BASE = "https://cmr.earthdata.nasa.gov/search"
    CMR_GRANULES = f"{CMR_BASE}/granules.json"
    CMR_COLLECTIONS = f"{CMR_BASE}/collections.json"
    
    # OB.DAAC (Ocean Biology)
    OBDAAC_BASE = "https://oceandata.sci.gsfc.nasa.gov/api/file_search"
    
    # GES DISC (Goddard Earth Sciences Data and Information Services Center)
    GESDISC_BASE = "https://disc.gsfc.nasa.gov/daac"
    
    # Default Search Parameters
    DEFAULT_PARAMS = {
        "pageSize": 10,
        "pageNum": 1,
        "sortBy": "acquisition_datetime",
        "sortOrder": "descending"
    }
    
    # EMIT-Specific Parameters for Mineral Detection
    EMIT_MINERAL_BANDS = {
        "Gold_Indicator": {"bands": [68, 69, 70], "wavelength_nm": "1650-1680"},
        "Alunite_Halo": {"bands": [50, 51], "wavelength_nm": "2125-2155"},
        "Calcite": {"bands": [85, 86], "wavelength_nm": "2305-2335"},
        "Muscovite": {"bands": [28, 29, 30], "wavelength_nm": "2320-2350"},
        "SWIR1": {"bands": [1, 100], "wavelength_nm": "1000-1350"},
        "SWIR2": {"bands": [100, 285], "wavelength_nm": "2000-2500"},
    }
    
    # Request Headers
    @staticmethod
    def get_auth_headers():
        """Returns properly formatted NASA authentication headers."""
        return {
            "Authorization": f"Bearer {NASAConfig.TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "OmniScan-XR2/1.0.0"
        }
    
    @staticmethod
    def get_request_timeout():
        """Returns request timeout in seconds."""
        return 30
    
    @staticmethod
    def validate_coordinates(lat: float, lon: float) -> bool:
        """Validates latitude and longitude ranges."""
        return -90 <= lat <= 90 and -180 <= lon <= 180
    
    @staticmethod
    def format_emit_search_params(lat: float, lon: float, page_size: int = 5) -> dict:
        """Formats parameters for EMIT search requests."""
        if not NASAConfig.validate_coordinates(lat, lon):
            raise ValueError(f"Invalid coordinates: {lat}, {lon}")
        
        return {
            "latitude": lat,
            "longitude": lon,
            "pageSize": page_size,
            "pageNum": 1,
            "sortBy": "cloud_cover_percentage"
        }


# Status Codes
API_RESPONSES = {
    200: "Success",
    400: "Bad Request",
    401: "Unauthorized (Token expired or invalid)",
    403: "Forbidden",
    404: "Resource Not Found",
    503: "Service Unavailable",
    504: "Gateway Timeout"
}
