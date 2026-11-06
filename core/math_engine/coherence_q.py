"""Модуль розрахунку Q-фактора та ефективної потужності P_eff.

Q-фактор за диференційним рівнянням:
    dQ/dt = α · (Q_target − Q) − β · Jitter + γ · Feedback

Класифікація зон когерентності:
    Зелений  : Q ≥ 0.90
    Жовтий   : 0.75 ≤ Q < 0.90
    Червоний : Q < 0.75

Ефективна потужність поля: P_eff = ‖E‖ × Q
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass(frozen=True)
class CoherenceZone:
    """Зона когерентності."""

    name: str
    q_min: float
    q_max: Optional[float]
    color: str

    def contains(self, q: float) -> bool:
        """Перевірити чи належить Q до цієї зони."""
        if self.q_max is None:
            return q >= self.q_min
        return self.q_min <= q < self.q_max


# Реєстр зон когерентності
COHERENCE_ZONES: tuple[CoherenceZone, ...] = (
    CoherenceZone(name="Зелений", q_min=0.90, q_max=None, color="green"),
    CoherenceZone(name="Жовтий", q_min=0.75, q_max=0.90, color="yellow"),
    CoherenceZone(name="Червоний", q_min=0.0, q_max=0.75, color="red"),
)


def classify_coherence_zone(q: float) -> CoherenceZone:
    """Класифікувати зону когерентності за значенням Q.

    Args:
        q: Значення Q-фактора (зазвичай [0.0, 1.0]).

    Returns:
        CoherenceZone об'єкт.
    """
    for zone in COHERENCE_ZONES:
        if zone.contains(q):
            return zone
    # Fallback: червона зона для будь-якого іншого значення
    return COHERENCE_ZONES[2]


def compute_q_factor(
    q_current: float,
    q_target: float,
    jitter: float,
    feedback: float,
    alpha: float = 0.1,
    beta: float = 0.05,
    gamma: float = 0.02,
    dt: float = 1.0,
) -> float:
    """Обчислити нове значення Q-фактора за диференційним рівнянням.

    dQ/dt = α · (Q_target − Q) − β · Jitter + γ · Feedback

    Args:
        q_current: Поточне значення Q.
        q_target:Цільове значення Q.
        jitter: Значення джиттера (шум).
        feedback: Зворотній зв'язок.
        alpha: Коефіцієнт притягу до цілі (за замовчуванням 0.1).
        beta: Коефіцієнт заглушення джиттером (за замовчуванням 0.05).
        gamma: Коефіцієнт зворотного зв'язку (за замовчуванням 0.02).
        dt: Крок часу (за замовчуванням 1.0).

    Returns:
        Оновлене значення Q-фактора.
    """
    dq_dt = alpha * (q_target - q_current) - beta * jitter + gamma * feedback
    q_new = q_current + dq_dt * dt
    # Обмеження Q у діапазоні [0.0, 1.0]
    return float(max(0.0, min(1.0, q_new)))


def compute_peff(e_norm: float, q: float) -> float:
    """Обчислити ефективну потужність поля: P_eff = ‖E‖ × Q.

    Args:
        e_norm: Норма 4D-вектора середовища ‖E‖.
        q: Q-фактор.

    Returns:
        Ефективна потужність P_eff.
    """
    return float(e_norm * q)


class CoherenceCalculator:
    """Керуючий клас для розрахунку когерентності та P_eff."""

    def __init__(
        self,
        alpha: float = 0.1,
        beta: float = 0.05,
        gamma: float = 0.02,
    ) -> None:
        """Ініціалізація калькулятора когерентності.

        Args:
            alpha: Коефіцієнт притягу до цілі.
            beta: Коефіцієнт заглушення джиттером.
            gamma: Коефіцієнт зворотного зв'язку.
        """
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def update_q(
        self,
        q_current: float,
        q_target: float,
        jitter: float,
        feedback: float,
        dt: float = 1.0,
    ) -> float:
        """Оновити Q-фактор за одного кроку часу."""
        return compute_q_factor(
            q_current=q_current,
            q_target=q_target,
            jitter=jitter,
            feedback=feedback,
            alpha=self.alpha,
            beta=self.beta,
            gamma=self.gamma,
            dt=dt,
        )

    def zone(self, q: float) -> CoherenceZone:
        """Отримати зону когерентності для значення Q."""
        return classify_coherence_zone(q)

    def peff(self, e_norm: float, q: float) -> float:
        """Обчислити P_eff = ‖E‖ × Q."""
        return compute_peff(e_norm=e_norm, q=q)