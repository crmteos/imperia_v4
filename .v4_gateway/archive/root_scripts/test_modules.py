"""Test Module for Imperia v4"""

import sys
import os

sys.path.insert(0, r"c:\imperia_v4\src")

def test_h3_vector():
    from geo.h3_vector_fresh import gps_to_h3_index, calculate_environment_vector, calculate_vector_at_resolutions
    lat, lon = 40.7128, -74.0060
    index = gps_to_h3_index(lat, lon, 9)
    assert index is not None
    print(f"  ✓ H3 index: {index}")
    vec = calculate_environment_vector(lat, lon)
    assert vec is not None
    print(f"  ✓ Environment vector calculated")
    indices = calculate_vector_at_resolutions(lat, lon, [4, 7, 9])
    assert len(indices) == 3
    print(f"  ✓ Multi-resolution indices: {list(indices.keys())}")
    return True

def test_resource_governor():
    from governor.resource_governor import ResourceGovernor
    governor = ResourceGovernor()
    assert governor.mode == "PERFORMANCE"
    print(f"  ✓ Initial mode: {governor.mode}")
    result = governor.update_metrics(battery_pct=10, temperature_celsius=35.0)
    assert governor.mode == "CRITICAL"
    print(f"  ✓ Critical mode: {governor.mode}")
    result = governor.update_metrics(battery_pct=80, temperature_celsius=35.0)
    assert governor.mode == "PERFORMANCE"
    print(f"  ✓ Normal mode: {governor.mode}")
    report = governor.get_status_report()
    assert "mode" in report and "battery_pct" in report
    print(f"  ✓ Status report available")
    return True

def test_stateful_ram():
    from context.stateful_ram import StatefulContextRAM
    ram = StatefulContextRAM(max_token_budget=8192)
    status = ram.get_status()
    assert status["max_token_budget"] == 8192
    assert status["total_tokens"] == 0
    print(f"  ✓ RAM initialized: budget=8192, tokens=0")
    vec = ram.update_vector_E(E_geo="index123", E_resource=0.5, E_coherence=0.8, E_temporal=1000)
    assert vec["E_geo"] == "index123"
    print(f"  ✓ Vector E updated")
    success = ram.allocate_tokens("state", 50)
    assert success
    status = ram.get_status()
    assert status["state_tokens"] == 50
    print(f"  ✓ Allocated 50 state tokens")
    success = ram.add_to_ephemeral({"key": "val"})
    assert success
    result = ram.get_ephemeral_next()
    assert result["data"] is not None
    print(f"  ✓ Ephemeral queue FIFO works")
    return True

def test_transport_adapter():
    from p2p.transport_adapter_fresh import TransportAdapter
    adapter = TransportAdapter(node_id="node-001")
    status = adapter.get_status()
    assert adapter.node_id == "node-001"
    assert adapter.connection_status == "disconnected"
    print(f"  ✓ Transport adapter initialized")
    success = adapter.connect_to_peer("peer-1", "192.168.1.1:8080")
    assert success
    status = adapter.get_status()
    assert status["active_peers"] == 1
    print(f"  ✓ Connected to peer-1")
    success = adapter.send_message("peer-1", {"type": "heartbeat"})
    assert success
    status = adapter.get_status()
    assert status["buffer_size"] == 1
    print(f"  ✓ Message sent and buffered")
    msg = adapter.receive_message()
    assert "_id" in msg
    print(f"  ✓ Message received")
    adapter.disconnect_peer("peer-1")
    status = adapter.get_status()
    assert status["active_peers"] == 0
    print(f"  ✓ Peer disconnected")
    return True

def main():
    print("Imperia v4 Module Tests")
    print("=" * 40)
    tests = [("H3 Vector", test_h3_vector), ("Resource Governor", test_resource_governor),
             ("Stateful RAM", test_stateful_ram), ("Transport Adapter", test_transport_adapter)]
    passed = failed = 0
    for name, func in tests:
        print(f"\n--- {name} ---")
        try:
            if func():
                passed += 1
                print(f"✓ {name} PASSED")
        except Exception as e:
            failed += 1
            print(f"✗ {name} FAILED: {e}")
    print(f"\nResults: {passed} passed, {failed} failed")
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())