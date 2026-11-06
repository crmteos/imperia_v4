"""Imperia v4 Math Engine Core — фасадна точка входу математичного ядра.

Експортує ключові класи та функції з усіх підмодулів:
- h3_grid: H3-індексація та просторова кластеризація
- coherence_q: Q-фактор та ефективна потужність P_eff
- vectors_e: 4D-вектор середовища E
- wave_physics: 6D хвильова фізика та інваріанти
"""

from .h3_grid import (
    H3Grid,
    latlng_to_h3,
    octave_to_h3_resolution,
    H3_OCTAVE_RES_MAP,
)
from .coherence_q import (
    CoherenceCalculator,
    CoherenceZone,
    compute_q_factor,
    compute_peff,
    classify_coherence_zone,
)
from .vectors_e import (
    EnvironmentVector,
    RegionalHub,
    REGIONAL_HUBS,
    vector_norm,
    get_hub_by_name,
)
from .wave_physics import (
    WavePhysics,
    compute_6d_power_invariant,
    jitterbug_angle,
    jitterbug_angle_rad,
    adler_phase_derivative,
    adler_phase_step,
)

__all__ = [
    # h3_grid
    "H3Grid",
    "latlng_to_h3",
    "octave_to_h3_resolution",
    "H3_OCTAVE_RES_MAP",
    # coherence_q
    "CoherenceCalculator",
    "CoherenceZone",
    "compute_q_factor",
    "compute_peff",
    "classify_coherence_zone",
    # vectors_e
    "EnvironmentVector",
    "RegionalHub",
    "REGIONAL_HUBS",
    "vector_norm",
    "get_hub_by_name",
    # wave_physics
    "WavePhysics",
    "compute_6d_power_invariant",
    "jitterbug_angle",
    "jitterbug_angle_rad",
    "adler_phase_derivative",
    "adler_phase_step",
]

__version__ = "1.0.0"