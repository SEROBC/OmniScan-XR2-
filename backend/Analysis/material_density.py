# ==============================================================================
# PROPRIETARY AND CONFIDENTIAL
# OmniScan-XR System - Copyright (c) 2026 Serob Cholakyan
# ==============================================================================

import json
import os

class SpectralAnalyzer:
    def __init__(self):
        # Use absolute path relative to this file's location
        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        lib_path = os.path.join(backend_dir, 'Data', 'spectral_lib.json')
        
        # Fallback to root-level Data if backend Data doesn't exist
        if not os.path.exists(lib_path):
            root_lib = os.path.join(os.path.dirname(backend_dir), 'Data', 'spectral_lib.json')
            if os.path.exists(root_lib):
                lib_path = root_lib
        
        if not os.path.exists(lib_path):
            raise FileNotFoundError(f"Spectral library not found at {lib_path}")
            
        with open(lib_path, 'r') as f:
            self.library = json.load(f)

    def calculate_absorption_depth(self, reflectance_center, reflectance_continuum):
        """Calculates absorption depth D = 1 - (R_center / R_continuum)"""
        if reflectance_continuum == 0:
            return 0
        return 1 - (reflectance_center / reflectance_continuum)

    def analyze_signature(self, swir1, swir2):
        """Evaluates mineral presence based on SWIR bands."""
        results = []
        for mineral in self.library['minerals']:
            ratio = swir1 / swir2 if swir2 != 0 else 0
            if ratio > mineral['probability_weight']:
                results.append({
                    "mineral": mineral['name'],
                    "confidence": min(ratio, 0.99)
                })
        return results
