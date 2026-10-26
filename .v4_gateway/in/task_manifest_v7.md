# Task Manifest v7: Step C — Social Media Broadcasting & Signal Collection Pipeline

## Objective
Implement social platform broadcasting agents (`src/smm_broadcaster.py`) and OSINT signal collection ingestion (`src/signal_collector.py`), enabling automated content distribution to channels (Telegram, Webhooks, Feeds) and automated updating of territory passports in `data/territories/`.

## Action Items

1. **Implement `src/smm_broadcaster.py`**:
   - Create asynchronous broadcasting class `SMMBroadcaster`.
   - Support formatters for Telegram Bot API payloads, Webhook JSONs, and Markdown social posts.
   - Connect to `src/kancelyariya_facade.py` telemetry and state updates.
   - Include dry-run mode for offline/test environments.

2. **Implement `src/signal_collector.py`**:
   - Create `SignalCollector` class for parsing raw OSINT items/signals.
   - Validate incoming signals against `data/manifest.json` schemas and `data/regions.json` primary keys.
   - Append verified signals to corresponding territory passport files in `data/territories/`.

3. **Create Test Suite `tests/test_step_c_broadcasting.py`**:
   - Test signal ingestion, schema validation, and region mapping.
   - Test dry-run message formatting and broadcasting.

4. **Git Operations & Execution State**:
   - Run tests: `pytest tests/test_step_c_broadcasting.py`.
   - Commit: `git commit -m "imperia_v4: Step C Social Broadcasting & Signal Collector complete"`.
   - Push to `main` branch on GitHub.
   - Update `.v4_gateway/out/execution_state.json`.
