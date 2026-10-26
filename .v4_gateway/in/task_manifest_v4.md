# Imperia v4 - Task Manifest (Phase 7: Kancelyariya Presentation Facade)

## Objective
Implement Phase 7: Kancelyariya Presentation Facade and UI Integration layer (`src/kancelyariya_facade.py` and `src/portal_bridge.py`). This facade translates P2P swarm vectors $\vec{E}$, Context RAM invariants, and node health into clean, client-side UI data models without anthropomorphic bias.

## Steps for AI Developer (Cline)

1. **Read Specifications**:
   - Inspect `.v4_gateway/in/architect_spec_v4.json` for module definitions and interfaces.

2. **Implement Facade & Portal Bridge Modules**:
   - `src/kancelyariya_facade.py`: Implement translation layer for $\vec{E}$ vector -> UI telemetry, Context RAM telemetry, and P2P node status.
   - `src/portal_bridge.py`: Implement static JSON telemetry exporter for local/GitHub Pages frontend consumption.

3. **Run Validation & Test Suite**:
   - Create and execute `tests/test_phase_7_facade.py`.
   - Ensure 100% pass rate across vector translations, status formatting, and static JSON schema generation.

4. **Git Commit & Execution State**:
   - Commit code to Git (`imperia_v4: Phase 7 Kancelyariya Facade complete`).
   - Push updates to remote repository (`git push origin main`).
   - Update `.v4_gateway/out/execution_state.json` with Phase 7 completion metrics.
