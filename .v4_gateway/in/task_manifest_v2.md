# TASK MANIFEST v4.1: Integration Testing & P2P Swarm Protocol

## 1. Goal
Implement P2P Swarm Inference Handoff and E2E Integration Suite for `imperia_v4`.

## 2. Tasks for Cline
1. Create `src/swarm_inference.py`:
   - Implement `InferenceQuantum` dataclass (quantum_id, h3_index, payload, poi_hash).
   - Implement `SwarmCoordinator` class managing P2P quantum dispatch between nodes.
2. Create `src/edge_handoff.py`:
   - Connect `ResourceGovernor` state transitions (e.g. `CRITICAL`) to dynamic P2P context handoff.
3. Create `tests/test_integration.py`:
   - Simulate 3 Edge Nodes in H3 cell (Resolution 7).
   - Verify task handoff during simulated battery drain and network shift.
4. Update `.v4_gateway/out/execution_state.json`:
   - Write output test summary, coverage percentage, and execution timestamps.
