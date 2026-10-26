"""H3 Geospatial Indexing and Environment Vector Calculation"""

import math
import time


def gps_to_h3_index(lat: float, lon: float, resolution: int) -> str:
    """Convert GPS coordinates to H3 index at the specified resolution."""
    try:
        import h3 as h3_lib
        index = h3_lib.geo_to_h3(lat, lon, resolution)
        return str(index)
    except ImportError:
        index_base = int(lat * 10000) ^ int(lon * 10000) % (2 ** 30)
        return f"h3_res{resolution}_{index_base:x}"


def calculate_environment_vector(lat: float, lon: float) -> dict:
    """Calculate the environment vector E = [E_geo, E_resource, E_coherence, E_temporal]."""
    e_geo = gps_to_h3_index(lat, lon, 9)
    resource_value = 0.5
    if -33.8 <= lat <= 52.5:
        resource_value = 0.7
    coherence_value = round(0.85 + 0.1 * math.sin(math.radians(lat)), 4)
    temporal_value = int(time.time())
    return {
        "E_geo": {"type": "string", "value": e_geo, "description": "H3 index at Res 9"},
        "E_resource": {"type": "number", "minimum": 0.0, "maximum": 1.0,
                       "value": round(resource_value, 4), "description": "Resource availability index"},
        "E_coherence": {"type": "number", "description": "Q-factor phase coherence", "value": coherence_value},
        "E_temporal": {"type": "integer", "description": "Unix Epoch timestamp", "value": temporal_value}
    }


def calculate_vector_at_resolutions(lat: float, lon: float, resolutions: list = None) -> dict:
    """Calculate H3 indices at multiple resolutions."""
    if resolutions is None:
        resolutions = [4, 7, 9]
    indices = {}
    for res in resolutions:
        try:
            index = gps_to_h3_index(lat, lon, res)
            indices[f"res_{res}"] = index
        except Exception:
            indices[f"res_{res}"] = f"fallback_h3_res{res}"
    return indices