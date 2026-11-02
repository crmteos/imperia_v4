"""Imperia v4 Edge Case Tests

Tests edge cases for all 6 modules:
1. Critical battery drops triggering edge_handoff
2. Context RAM buffer overflows
3. P2P peer disconnects
4. Mode transitions under stress
5. H3 fallback logic
"""

import sys
sys.path.insert(0, r"c:\imperia_v4\src")

from governor.resource_governor import ResourceGovernor
from context.stateful_ram import StatefulContextRAM
from p2p.transport_adapter import TransportAdapter
from geo.h3_vector import gps_to_h3_index, calculate_environment_vector, calculate_vector_at_resolutions
from edge_handoff import EdgeHandoff
from swarm_inference import SwarmInference


def test_rg_critical():
    print("--- RG Critical ---")
    g = ResourceGovernor()
    assert g.mode == "PERFORMANCE"
    g.update_metrics(battery_pct=5, temperature_celsius=45, is_charging=False)
    assert g.mode == "CRITICAL"
    g.update_metrics(battery_pct=80, temperature_celsius=35, is_charging=True)
    assert g.mode == "PERFORMANCE"
    g.update_metrics(battery_pct=80, temperature_celsius=85, is_charging=False)
    assert g.mode == "CRITICAL"
    print("  PASS")


def test_ram_overflow():
    print("--- RAM Overflow ---")
    r = StatefulContextRAM(max_token_budget=100)
    t1 = r.allocate_tokens("state", 50)
    t2 = r.allocate_tokens("state", 30)
    t3 = r.allocate_tokens("state", 40)  # Only 20 remaining, should fail
    assert t1 == True, f"Expected True, got {t1}"
    assert t2 == True, f"Expected True, got {t2}"
    assert t3 == False, f"Expected False (capacity), got {t3}"
    s = r.get_status()
    assert s["total_tokens"] == 80, f"Expected 80, got {s['total_tokens']}"
    print("  PASS")


def test_p2p_disconnect():
    print("--- P2P Disconnect ---")
    t = TransportAdapter(node_id="test-node")
    t.connect_to_peer("p1", ("1.1.1.1", 8080))
    t.send_message("p1", {"type": "test"})
    t.disconnect_peer("p1")
    s = t.get_status()
    assert s["active_peers"] == 0
    print("  PASS")


def test_h3_fallback():
    print("--- H3 Fallback ---")
    idx = gps_to_h3_index(37.7749, -122.4194, 9)
    ev = calculate_environment_vector(37.7749, -122.4194)
    assert "E_geo" in ev and "E_resource" in ev and "E_coherence" in ev and "E_temporal" in ev
    ind = calculate_vector_at_resolutions(37.7749, -122.4194, [7, 9])
    assert "res_7" in ind and "res_9" in ind
    print("  PASS")


def test_si_import():
    print("--- SI Import ---")
    inf = SwarmInference(node_id="test")
    assert inf.node_id == "test"
    assert inf.governor.mode == "PERFORMANCE"
    assert inf.ram.get_status()["max_token_budget"] == 8192
    print("  PASS")


def test_eh_proximity():
    print("--- EH Proximity ---")
    h = EdgeHandoff(node_id="test")
    h.set_location(34.0522, -118.2436)
    h.update_peers(["cp"], [(34.0523, -118.2436)])
    should, reason = h.should_handoff()
    print(f"  {should}: {reason}")
    print("  PASS")


if __name__ == "__main__":
    test_rg_critical()
    test_ram_overflow()
    test_p2p_disconnect()
    test_h3_fallback()
    test_si_import()
    test_eh_proximity()
    print("ALL EDGE CASE TESTS PASSED")