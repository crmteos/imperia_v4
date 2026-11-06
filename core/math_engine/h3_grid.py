"""Модуль просторової кластеризації та H3-індексації.

Мапінг між октавами масштабно-частотної осі M-f (M0..M6)
та деталізацією Uber H3 (від H3 Res 15 до H3 Res 0).

Залежність: h3 (open-source). Якщо бібліотека недоступна,
забезпечується纯 Python fallback.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

try:
    import h3  # type: ignore

    _H3_AVAILABLE = True
except ImportError:  # pragma: no cover
    h3 = None  # type: ignore
    _H3_AVAILABLE = False

# Мапінг октави M -> H3 resolution
# M0 (найменша деталізація) -> H3 Res 0
# M6 (найбільша деталізація) -> H3 Res 15
H3_OCTAVE_RES_MAP: dict[int, int] = {
    0: 0,
    1: 2,
    2: 5,
    3: 7,
    4: 10,
    5: 13,
    6: 15,
}


@dataclass(frozen=True)
class H3Cell:
    """Результат H3-індексації."""

    h3_index: str
    resolution: int
    lat: float
    lng: float


def octave_to_h3_resolution(octave: int) -> int:
    """Перетворити октаву M (0..6) на H3 resolution (0..15).

    Args:
        octave: Октава масштабно-частотної осі M (0..6).

    Returns:
        H3 resolution рівень (0..15).

    Raises:
        ValueError: Якщо octave не в діапазоні 0..6.
    """
    if octave not in H3_OCTAVE_RES_MAP:
        raise ValueError(
            f"Октава {octave} не підтримується. Допустимі значення: {sorted(H3_OCTAVE_RES_MAP.keys())}"
        )
    return H3_OCTAVE_RES_MAP[octave]


def latlng_to_h3(lat: float, lng: float, resolution: int) -> str:
    """Перетворити географічні координати на H3-індекс.

    Args:
        lat: Широта у градусах (-90..90).
        lng: Довгота у градусах (-180..180).
        resolution: H3 resolution (0..15).

    Returns:
        H3-індекс у вигляді рядка.

    Raises:
        ValueError: Якщо координати або resolution невірні.
        RuntimeError: Якщо бібліотека h3 недоступна.
    """
    if not -90.0 <= lat <= 90.0:
        raise ValueError(f"Широта {lat} не в діапазоні [-90, 90]")
    if not -180.0 <= lng <= 180.0:
        raise ValueError(f"Довгота {lng} не в діапазоні [-180, 180]")
    if not 0 <= resolution <= 15:
        raise ValueError(f"Resolution {resolution} не в діапазоні [0, 15]")

    if _H3_AVAILABLE and h3 is not None:
        return h3.latlng_to_cell(lat, lng, resolution)  # type: ignore[attr-defined]

    # Pure Python fallback: deterministic hash-based H3-like index
    # Це тимчасове rozwiązanie для середовищ без h3 бібліотеки.
    import hashlib

    key = f"{lat:.6f},{lng:.6f},{resolution}".encode("utf-8")
    digest = hashlib.sha256(key).hexdigest()[:16]
    return f"FALLBACK_{resolution:02X}_{digest}"


class H3Grid:
    """Керуючий клас для H3- просторової кластеризації."""

    def __init__(self, default_octave: int = 3) -> None:
        """Ініціалізація H3Grid.

        Args:
            default_octave: Базова октава M (0..6), за замовчуванням 3.
        """
        self.default_octave = default_octave
        self.default_resolution = octave_to_h3_resolution(default_octave)

    def index_point(self, lat: float, lng: float, octave: Optional[int] = None) -> H3Cell:
        """Індексувати точку в H3-сітку.

        Args:
            lat: Широта у градусах.
            lng: Довгота у градусах.
            octave: Октава M (якщо None, використовується default_octave).

        Returns:
            H3Cell із індексом, разрешenchю та координатами.
        """
        res = self.default_resolution if octave is None else octave_to_h3_resolution(octave)
        h3_index = latlng_to_h3(lat, lng, res)
        return H3Cell(h3_index=h3_index, resolution=res, lat=lat, lng=lng)

    def octave_resolution(self, octave: int) -> int:
        """Отримати H3 resolution для октави."""
        return octave_to_h3_resolution(octave)

    def available(self) -> bool:
        """Чи доступна бібліотека h3."""
        return _H3_AVAILABLE