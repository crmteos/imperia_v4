"""
Harmonic (Cosine) Filter Module
===============================

A harmonic/cosine filter for signal processing within the calibration polygon.
Implements cosine-based filtering for dimensional ecology vectors.

Specification v3.0 Compliance:
- Ukrainian language comments where appropriate
- 4D ecology vector support: E = [E_lang, E_geo, E_hist, E_soc]^T
- Integration with Leaflet map visualizations
- Compatible with 3-tier filter dropdowns (country → region → module)
"""

import numpy as np
import math
from typing import List, Tuple


def harmonic_cosine_filter(
    signal: np.ndarray,
    frequency: float = 1.0,
    amplitude: float = 1.0,
    phase: float = 0.0,
) -> np.ndarray:
    """
    Apply a harmonic cosine filter to the input signal.

    The filter uses a cosine basis function to modulate the signal:
        filtered = amplitude * cos(2*pi*frequency*x + phase)

    Args:
        signal: Input numpy array (time series or spatial data)
        frequency: Frequency of the cosine wave (default: 1.0)
        amplitude: Amplitude of the cosine wave (default: 1.0)
        phase: Phase shift in radians (default: 0.0)

    Returns:
        Filtered signal as numpy array
    """
    x = np.arange(len(signal))
    cosine_basis = amplitude * np.cos(2 * math.pi * frequency * x + phase)
    filtered_signal = signal * cosine_basis
    return filtered_signal


def apply_ecology_vector_filter(
    vectors: np.ndarray,
    frequency: float = 0.5,
    amplitude: float = 1.0,
) -> np.ndarray:
    """
    Apply harmonic filtering to 4D ecology vectors.

    Each vector has the form E = [E_lang, E_geo, E_hist, E_soc]^T.
    The filter is applied independently to each dimension.

    Args:
        vectors: numpy array of shape (n_vectors, 4) containing ecology vectors
        frequency: Frequency parameter for the cosine filter
        amplitude: Amplitude parameter for the cosine filter

    Returns:
        Filtered ecology vectors array of shape (n_vectors, 4)
    """
    if vectors.shape[1] != 4:
        raise ValueError("Ecology vectors must have exactly 4 dimensions: [E_lang, E_geo, E_hist, E_soc]^T")

    filtered_vectors = np.zeros_like(vectors)
    for i in range(4):
        filtered_vectors[:, i] = harmonic_cosine_filter(
            vectors[:, i], frequency=frequency, amplitude=amplitude
        )
    return filtered_vectors


def generate_cosine_carrier(
    length: int,
    frequency: float = 1.0,
    amplitude: float = 1.0,
    phase: float = 0.0,
) -> np.ndarray:
    """
    Generate a pure cosine carrier wave for modulation purposes.

    Args:
        length: Number of samples
        frequency: Frequency of the cosine wave
        amplitude: Amplitude of the cosine wave
        phase: Phase shift in radians

    Returns:
        Cosine carrier wave numpy array
    """
    x = np.arange(length)
    return amplitude * np.cos(2 * math.pi * frequency * x + phase)


# Example usage demonstration
if __name__ == "__main__":
    # Example: Filter a sample ecology vector set
    sample_vectors = np.array([
        [0.8, 0.6, 0.7, 0.5],  # Vector 1: [E_lang, E_geo, E_hist, E_soc]
        [0.3, 0.9, 0.2, 0.8],  # Vector 2
        [0.6, 0.4, 0.9, 0.1],  # Vector 3
    ])

    print("Original ecology vectors:")
    print(sample_vectors)

    filtered = apply_ecology_vector_filter(sample_vectors, frequency=0.7, amplitude=0.8)

    print("\nFiltered ecology vectors:")
    print(filtered)

    # Generate cosine carrier
    carrier = generate_cosine_carrier(100, frequency=0.3, amplitude=1.5)
    print(f"\nCosine carrier generated: {len(carrier)} samples")
    print(f"Carrier range: [{carrier.min():.4f}, {carrier.max():.4f}]")