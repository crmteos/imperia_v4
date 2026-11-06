"""Скрипт модульного тестування Math Engine Core.

Запуск: python core/math_engine/test_engine.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from core.math_engine import (  # noqa: E402
    H3_OCTAVE_RES_MAP,
    CoherenceZone,
    EnvironmentVector,
    RegionalHub,
    WavePhysics,
    adler_phase_derivative,
    classify_coherence_zone,
    compute_6d_power_invariant,
    compute_peff,
    compute_q_factor,
    get_hub_by_name,
    jitterbug_angle,
    jitterbug_angle_rad,
    adler_phase_step,
    latlng_to_h3,
    octave_to_h3_resolution,
    vector_norm,
)


def test_h3_grid() -> None:
    """Тести для h3_grid.py."""
    print("=== Тести h3_grid ===")

    assert H3_OCTAVE_RES_MAP[0] == 0
    assert H3_OCTAVE_RES_MAP[6] == 15
    assert len(H3_OCTAVE_RES_MAP) == 7
    print("  [OK] H3_OCTAVE_RES_MAP коректний")

    assert octave_to_h3_resolution(0) == 0
    assert octave_to_h3_resolution(3) == 7
    assert octave_to_h3_resolution(6) == 15
    try:
        octave_to_h3_resolution(7)
        assert False, "Повинен бути ValueError для октави 7"
    except ValueError:
        pass
    print("  [OK] octave_to_h3_resolution працює")

    h3_index = latlng_to_h3(50.4501, 30.5234, resolution=9)
    assert isinstance(h3_index, str)
    assert len(h3_index) > 0
    print(f"  [OK] latlng_to_h3(Київ, res=9) = {h3_index}")

    try:
        latlng_to_h3(91.0, 30.5234, resolution=9)
        assert False, "Повинен бути ValueError для широти 91"
    except ValueError:
        pass
    try:
        latlng_to_h3(50.4501, 181.0, resolution=9)
        assert False, "Повинен бути ValueError для довготи 181"
    except ValueError:
        pass
    try:
        latlng_to_h3(50.4501, 30.5234, resolution=20)
        assert False, "Повинен бути ValueError для resolution 20"
    except ValueError:
        pass
    print("  [OK] Валідація координат працює")

    from core.math_engine.h3_grid import H3Grid

    grid = H3Grid(default_octave=3)
    assert grid.default_resolution == 7
    cell = grid.index_point(50.4501, 30.5234)
    assert cell.resolution == 7
    assert cell.lat == 50.4501
    assert cell.lng == 30.5234
    assert isinstance(cell.h3_index, str)
    print("  [OK] H3Grid.class працює")

    from core.math_engine.h3_grid import _H3_AVAILABLE

    print(f"  [INFO] h3 бібліотека доступна: {_H3_AVAILABLE}")
    print()
def test_coherence_q() -> None:
    """Тести для coherence_q.py."""
    print("=== Тести coherence_q ===")

    q_new = compute_q_factor(
        q_current=0.5,
        q_target=0.9,
        jitter=0.1,
        feedback=0.2,
        alpha=0.1,
        beta=0.05,
        gamma=0.02,
        dt=1.0,
    )
    assert 0.0 <= q_new <= 1.0
    print(f"  [OK] compute_q_factor: Q={q_new:.4f}")

    q_clamped = compute_q_factor(
        q_current=0.99, q_target=1.0, jitter=0.0, feedback=1.0, dt=10.0
    )
    assert q_clamped <= 1.0
    q_clamped_low = compute_q_factor(
        q_current=0.01, q_target=0.0, jitter=1.0, feedback=0.0, dt=10.0
    )
    assert q_clamped_low >= 0.0
    print("  [OK] Q обмежений у [0, 1]")

    zone_green = classify_coherence_zone(0.95)
    assert zone_green.name == "Зелений"
    zone_yellow = classify_coherence_zone(0.80)
    assert zone_yellow.name == "Жовтий"
    zone_red = classify_coherence_zone(0.50)
    assert zone_red.name == "Червоний"
    print("  [OK] classify_coherence_zone працює")

    peff = compute_peff(e_norm=0.8, q=0.9)
    assert abs(peff - 0.72) < 1e-9
    print(f"  [OK] compute_peff: P_eff={peff}")

    from core.math_engine.coherence_q import CoherenceCalculator

    calc = CoherenceCalculator(alpha=0.1, beta=0.05, gamma=0.02)
    q_updated = calc.update_q(0.5, 0.9, 0.1, 0.2)
    assert 0.0 <= q_updated <= 1.0
    zone = calc.zone(0.95)
    assert zone.name == "Зелений"
    peff_val = calc.peff(0.8, 0.9)
    assert abs(peff_val - 0.72) < 1e-9
    print("  [OK] CoherenceCalculator.class працює")
    print()
def test_vectors_e() -> None:
    """Тести для vectors_e.py."""
    print("=== Тести vectors_e ===")

    vec = EnvironmentVector(e_lang=0.5, e_geo=0.6, e_hist=0.7, e_soc=0.8)
    assert vec.e_lang == 0.5
    assert vec.e_geo == 0.6
    assert vec.e_hist == 0.7
    assert vec.e_soc == 0.8
    print("  [OK] EnvironmentVector створюється")

    try:
        EnvironmentVector(e_lang=1.5, e_geo=0.5, e_hist=0.5, e_soc=0.5)
        assert False, "Повинен бути ValueError для e_lang=1.5"
    except ValueError:
        pass
    try:
        EnvironmentVector(e_lang=-0.1, e_geo=0.5, e_hist=0.5, e_soc=0.5)
        assert False, "Повинен бути ValueError для e_lang=-0.1"
    except ValueError:
        pass
    print("  [OK] Валідація компонент працює")

    import numpy as np

    arr = vec.to_array()
    assert isinstance(arr, np.ndarray)
    assert arr.shape == (4,)
    print("  [OK] to_array повертає np.ndarray")

    norm = vector_norm(vec)
    expected_norm = np.sqrt(0.5**2 + 0.6**2 + 0.7**2 + 0.8**2)
    assert abs(norm - expected_norm) < 1e-9
    print(f"  [OK] vector_norm: ‖E‖={norm:.6f}")

    normed = vec.normalized()
    normed_norm = vector_norm(normed)
    assert abs(normed_norm - 1.0) < 1e-6 or normed_norm == 0.0
    print(f"  [OK] normalized: ‖E_norm‖={normed_norm:.6f}")

    from core.math_engine.vectors_e import REGIONAL_HUBS, get_hub_by_name

    assert len(REGIONAL_HUBS) == 5
    print("  [OK] REGIONAL_HUBS містить 5 міст")

    kyiv = get_hub_by_name("Київ")
    assert kyiv.name == "Київ"
    assert abs(kyiv.lat - 50.4501) < 1e-4
    assert abs(kyiv.lng - 30.5234) < 1e-4
    print(f"  [OK] get_hub_by_name('Київ'): lat={kyiv.lat}, lng={kyiv.lng}")

    try:
        get_hub_by_name("НеіснуючеМісто")
        assert False, "Повинен бути KeyError"
    except KeyError:
        pass
    print("  [OK] KeyError для невідомого міста")
    print()
def test_wave_physics() -> None:
    """Тести для wave_physics.py."""
    print("=== Тести wave_physics ===")

    import numpy as np

    inv = compute_6d_power_invariant(length_scale=2.0, time_scale=1.0)
    assert abs(inv - 32.0) < 1e-9  # 2^5 / 1^5 = 32
    print(f"  [OK] 6D інваріант: L^5/T^5 = {inv}")

    try:
        compute_6d_power_invariant(length_scale=0.0, time_scale=1.0)
        assert False, "Повинен бути ValueError для L=0"
    except ValueError:
        pass
    print("  [OK] Валідація нульових значень працює")

    theta_0 = jitterbug_angle(phase=0.0, out_wave=True)
    assert abs(theta_0 - 0.0) < 1e-9
    theta_max = jitterbug_angle(phase=1.0, out_wave=True)
    assert abs(theta_max - 70.528779) < 1e-3
    theta_mid = jitterbug_angle(phase=0.5, out_wave=True)
    assert 0.0 < theta_mid < 70.528779
    print(f"  [OK] Jitterbug кут: θ(0)={theta_0}, θ(1)={theta_max:.4f}, θ(0.5)={theta_mid:.4f}")

    try:
        jitterbug_angle(phase=1.5)
        assert False, "Повинен бути ValueError для phase=1.5"
    except ValueError:
        pass
    print("  [OK] Валідація фази працює")

    theta_rad = jitterbug_angle_rad(phase=1.0, out_wave=True)
    assert abs(theta_rad - np.radians(70.528779)) < 1e-3
    print("  [OK] jitterbug_angle_rad працює")

    dphi = adler_phase_derivative(delta_phi=0.5, delta_omega=1.0, k=0.5)
    expected = 1.0 - 0.5 * np.sin(0.5)
    assert abs(dphi - expected) < 1e-9
    print(f"  [OK] Адлера похідна: d(Δφ)/dt = {dphi:.6f}")

    new_phi = adler_phase_step(delta_phi=0.5, delta_omega=1.0, k=0.5, dt=0.01)
    assert isinstance(new_phi, float)
    print(f"  [OK] Адлера крок: Δφ_new = {new_phi:.6f}")

    wp = WavePhysics()
    inv_wp = wp.power_invariant(2.0, 1.0)
    assert abs(inv_wp - 32.0) < 1e-9
    theta_wp = wp.jitterbug(phase=1.0, out_wave=True)
    assert abs(theta_wp - 70.528779) < 1e-3
    phi_wp = wp.adler(delta_phi=0.5, delta_omega=1.0, k=0.5, dt=0.01)
    assert isinstance(phi_wp, float)
    print("  [OK] WavePhysics.class працює")
    print()
def test_imports() -> None:
    """Тест імпортів з фасада __init__.py."""
    print("=== Тести імпортів ===")
    import core.math_engine as me

    assert hasattr(me, "latlng_to_h3")
    assert hasattr(me, "compute_q_factor")
    assert hasattr(me, "compute_peff")
    assert hasattr(me, "vector_norm")
    assert hasattr(me, "jitterbug_angle")
    assert hasattr(me, "adler_phase_derivative")
    assert hasattr(me, "H3Grid")
    assert hasattr(me, "CoherenceCalculator")
    assert hasattr(me, "EnvironmentVector")
    assert hasattr(me, "WavePhysics")
    assert hasattr(me, "REGIONAL_HUBS")
    assert hasattr(me, "__version__")
    print("  [OK] Усі імпорти з __init__.py працюють")
    print(f"  [INFO] Версія ядра: {me.__version__}")
    print()


def main() -> int:
    """Запустити всі тести."""
    print("🧪 Тестування Math Engine Core (Imperia v4)\n")

    failed = 0
    tests = [
        test_imports,
        test_h3_grid,
        test_coherence_q,
        test_vectors_e,
        test_wave_physics,
    ]

    for test_fn in tests:
        try:
            test_fn()
        except Exception as exc:  # noqa: BLE001
            print(f"  [FAIL] {test_fn.__name__}: {exc}\n")
            failed += 1

    print("=" * 40)
    if failed == 0:
        print("✅ Усі тести пройшли успішно!")
        return 0
    print(f"❌ {failed} тест(ів) не пройдено.")
    return 1


if __name__ == "__main__":
    sys.exit(main())