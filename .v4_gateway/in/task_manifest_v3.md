# TASK MANIFEST v3.0: Phase 6 Real P2P Transport & GitHub Integration

## Objectives
1. Set up GitHub remote repository integration for `C:\imperia_v4`.
2. Implement production-ready asynchronous P2P transport adapter (`src/real_p2p_transport.py`).
3. Create unified protocol bridge (`src/p2p_protocol_bridge.py`) integrating real networking with `swarm_inference` and `edge_handoff`.
4. Validate asynchronously with `tests/test_phase_6_transport.py`.

---

## Task Instructions for Cline / VS Code AI

### Step 1: GitHub Repository Setup
Execute the following commands in PowerShell/Bash inside `C:\imperia_v4`:
```bash
git remote add origin <YOUR_GITHUB_REPO_URL>
git branch -M main
git push -u origin main
```
*(If remote is already set, verify status with `git status`)*.

### Step 2: Implementation of `src/real_p2p_transport.py`
* Implement `AsyncP2PNode` using `asyncio` and `websockets` or native sockets.
* Bind messaging to H3 Res 7 topics (`/v4/h3/{h3_meso}`).
* Implement Resource Governor integration (automatically drop/limit connection pool on `CRITICAL` resource mode).

### Step 3: Implementation of `src/p2p_protocol_bridge.py`
* Wrap both `p2p_transport.py` (simulated) and `real_p2p_transport.py` (networked) behind `UnifiedTransportAdapter`.
* Ensure `edge_handoff.py` can serialize context snapshots and transmit them over active WebSocket/socket sessions.

### Step 4: Verification Suite
* Create and run `tests/test_phase_6_transport.py`.
* Ensure async event loop tests pass 100%.
* Update `.v4_gateway/out/execution_state.json` with status `"phase_6_transport_complete"`.
