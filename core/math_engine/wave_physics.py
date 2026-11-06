"""Модуль 6D хвильової фізики (3L, 3T).

Обчислення 6D інваріанта потужності [L^5 T^-5] = Const.

Траєкторія кута повороту Джиттербагу Фуллера θ ∈ [0°, 70.53°]
між Out-Wave (Кубоктаедр) та In-Wave (Тетраедр).

Рівняння Адлера для фазового затягування:
    d(Δφ)/dt = Δω − K · sin(Δφ)
"""

from __future__ import annotations

import numpy as np

# Константа Джиттербагу Фуллера: кут між Кубоктаедром та Тетраедром
JITTERBUG_MAX_ANGLE_DEG: float = 70.528779  # ≈ 70.53°
JITTERBUG_MAX_ANGLE_RAD: float = np.radians(JITTERBUG_MAX_ANGLE_DEG)

# 6D invariant constant (потужність у [L^5 T^-5])
SIXD_POWER_CONSTANT: float = 1.0


def compute_6d_power_invariant(
    length_scale: float,
    time_scale: float,
) -> float:
    """Обчислити 6D інваріант потужності [L^5 T^-5] = Const.

    Args:
        length_scale: Characteristic length scale L.
        time_scale: Characteristic time scale T.

    Returns:
        Значення інваріанта потужності у одиницях [L^5 T^-5].
    """
    if length_scale == 0 or time_scale == 0:
        raise ValueError("length_scale та time_scale повинні бути ненульовими")
    invariant = (length_scale**5) / (time_scale**5)
    return float(invariant)


def jitterbug_angle(
    phase: float,
    out_wave: bool = True,
) -> float:
    """Обчислити кут повороту Джиттербагу Фуллера θ ∈ [0°, 70.53°].

    Модель переходу між Out-Wave (Кубоктаедр) та In-Wave (Тетраедр).
    При phase=0 → θ=0° (Кубоктаедр), при phase=1 → θ=70.53° (Тетраедр).

    Args:
        phase: Фаза переходу [0.0, 1.0].
        out_wave: Чи напрямок у Out-Wave (True) або In-Wave (False).

    Returns:
        Кут θ у градусах [0, 70.53].
    """
    if not 0.0 <= phase <= 1.0:
        raise ValueError(f"Фаза {phase} не в діапазоні [0.0, 1.0]")
    theta_deg = JITTERBUG_MAX_ANGLE_DEG * phase
    if not out_wave:
        theta_deg = JITTERBUG_MAX_ANGLE_DEG - theta_deg
    return float(theta_deg)


def jitterbug_angle_rad(phase: float, out_wave: bool = True) -> float:
    """Обчислити кут Джиттербагу у радіанах."""
    return float(np.radians(jitterbug_angle(phase=phase, out_wave=out_wave)))


def adler_phase_derivative(
    delta_phi: float,
    delta_omega: float,
    k: float,
) -> float:
    """Обчислити похідну фазового затягування за рівнянням Адлера.

    d(Δφ)/dt = Δω − K · sin(Δφ)

    Args:
        delta_phi: Фазова різниця Δφ у радіанах.
        delta_omega: Різниця кутових частот Δω.
        k: Коефіцієнт з'єднання K.

    Returns:
        Похідна d(Δφ)/dt.
    """
    return float(delta_omega - k * np.sin(delta_phi))


def adler_phase_step(
    delta_phi: float,
    delta_omega: float,
    k: float,
    dt: float = 0.01,
) -> float:
    """Зробити один крок інтеграції рівняння Адлера (метод Ейлера).

    Args:
        delta_phi: Поточна фазова різниця Δφ у радіанах.
        delta_omega: Різниця кутових частот Δω.
        k: Коефіцієнт з'єднання K.
        dt: Крок часу.

    Returns:
        Нова фазова різниця Δφ.
    """
    dphi_dt = adler_phase_derivative(delta_phi, delta_omega, k)
    return float(delta_phi + dphi_dt * dt)


class WavePhysics:
    """Керуючий клас для 6D хвильової фізики."""

    def __init__(self, invariant_constant: float = SIXD_POWER_CONSTANT) -> None:
        """Ініціалізація WavePhysics.

        Args:
            invariant_constant: Константа 6D інваріанта.
        """
        self.invariant_constant = invariant_constant

    def power_invariant(self, length_scale: float, time_scale: float) -> float:
        """Обчислити 6D інваріант потужності."""
        return compute_6d_power_invariant(length_scale, time_scale)

    def jitterbug(self, phase: float, out_wave: bool = True) -> float:
        """Обчислити кут Джиттербагу у градусах."""
        return jitterbug_angle(phase=phase, out_wave=out_wave)

    def adler(
        self,
        delta_phi: float,
        delta_omega: float,
        k: float,
        dt: float = 0.01,
    ) -> float:
        """Один крок інтеграції рівняння Адлера."""
        return adler_phase_step(delta_phi, delta_omega, k, dt=dt)