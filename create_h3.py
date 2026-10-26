#!/usr/bin/env python3
import os

# Create directories
for d in ['c:\imperia_v4\src\geo', 'c:\imperia_v4\src\governor', 
          'c:\imperia_v4\src\context', 'c:\imperia_v4\src\p2p']:
    os.makedirs(d, exist_ok=True)

# h3_vector.py - first half
h3v_content = '''"""H3 Geospatial Indexing and Environment Vector Calculation"""

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
'''

with open('c:\\imperia_v4\\src\\geo\\h3_vector.py', 'w') as f:
    f.write(h3v_content)

print("h3_vector.py created (partial)")