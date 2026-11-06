"""Модуль 4D-вектора середовища E.

Структура: E = [E_lang, E_geo, E_hist, E_soc]^T
з нормалізацією компонент у [0.0, 1.0].

Функція обчислення норми ‖E‖.

Реєстр канонічних регіональних хабів: Київ, Львів, Одеса, Харків, Дніпро.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import numpy as np


@dataclass(frozen=True)
class EnvironmentVector:
    """4D-вектор середовища E = [E_lang, E_geo, E_hist, E_soc]^T."""

    e_lang: float
    e_geo: float
    e_hist: float
    e_soc: float

    def __post_init__(self) -> None:
        """Валідація компонент у діапазоні [0.0, 1.0]."""
        for name, value in (
            ("e_lang", self.e_lang),
            ("e_geo", self.e_geo),
            ("e_hist", self.e_hist),
            ("e_soc", self.e_soc),
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"Компонента {name}={value} не в діапазоні [0.0, 1.0]")

    def to_array(self) -> np.ndarray:
        """Повернути вектор як numpy масив."""
        return np.array([self.e_lang, self.e_geo, self.e_hist, self.e_soc], dtype=float)

    def as_tuple(self) -> tuple[float, float, float, float]:
        """Повернути веktor як кортеж."""
        return (self.e_lang, self.e_geo, self.e_hist, self.e_soc)

    def normalized(self) -> "EnvironmentVector":
        """Повернути нормалізовану копію вектора (компоненти в [0, 1])."""
        arr = self.to_array()
        norm = float(np.linalg.norm(arr))
        if norm == 0.0:
            return EnvironmentVector(0.0, 0.0, 0.0, 0.0)
        normalized_arr = arr / norm
        # Кламп до [0, 1] після нормалізації
        normalized_arr = np.clip(normalized_arr, 0.0, 1.0)
        return EnvironmentVector(
            e_lang=float(normalized_arr[0]),
            e_geo=float(normalized_arr[1]),
            e_hist=float(normalized_arr[2]),
            e_soc=float(normalized_arr[3]),
        )


def vector_norm(vec: EnvironmentVector) -> float:
    """Обчислити евклідову норму ‖E‖ 4D-вектора.

    Args:
        vec: EnvironmentVector об'єкт.

    Returns:
        Норма ‖E‖.
    """
    return float(np.linalg.norm(vec.to_array()))


@dataclass(frozen=True)
class RegionalHub:
    """Канонічний регіональний хаб."""

    name: str
    lat: float
    lng: float
    vector: EnvironmentVector


# Реєстр канонічних регіональних хабів України
REGIONAL_HUBS: List[RegionalHub] = [
    RegionalHub(
        name="Київ",
        lat=50.4501,
        lng=30.5234,
        vector=EnvironmentVector(e_lang=0.95, e_geo=0.80, e_hist=0.90, e_soc=0.85),
    ),
    RegionalHub(
        name="Львів",
        lat=49.8429,
        lng=24.0311,
        vector=EnvironmentVector(e_lang=0.98, e_geo=0.70, e_hist=0.95, e_soc=0.80),
    ),
    RegionalHub(
        name="Одеса",
        lat=46.4825,
        lng=30.7233,
        vector=EnvironmentVector(e_lang=0.85, e_geo=0.90, e_hist=0.85, e_soc=0.88),
    ),
    RegionalHub(
        name="Харків",
        lat=49.9935,
        lng=36.2304,
        vector=EnvironmentVector(e_lang=0.80, e_geo=0.75, e_hist=0.80, e_soc=0.90),
    ),
    RegionalHub(
        name="Дніпро",
        lat=48.4647,
        lng=35.0462,
        vector=EnvironmentVector(e_lang=0.82, e_geo=0.78, e_hist=0.75, e_soc=0.82),
    ),
]


def get_hub_by_name(name: str) -> RegionalHub:
    """Отримати хаб за назвою міста.

    Args:
        name: Назва міста (Київ, Львів, Одеса, Харків, Дніпро).

    Returns:
        RegionalHub об'єкт.

    Raises:
        KeyError: Якщо місто не знайдено в реєстрі.
    """
    for hub in REGIONAL_HUBS:
        if hub.name.lower() == name.lower():
            return hub
    raise KeyError(f"Регіональний хаб '{name}' не знайдено у реєстрі")


def hub_dict() -> Dict[str, RegionalHub]:
    """Повернути реєстр хабів як словник {місто: RegionalHub}."""
    return {hub.name: hub for hub in REGIONAL_HUBS}