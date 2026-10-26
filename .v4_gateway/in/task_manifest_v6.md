# Imperia v4: Task Manifest — Step B (Database & OSINT Passports Framework)

## Objective
Establish the relational OSINT data framework, regional registry with integer primary keys, central schema manifest, and automated schema validation script as specified in `AI_CONTEXT_GATEWAY.md`.

## Execution Steps for Cline

1. **Create Central Manifest Registry (`data/manifest.json`)**:
   - Define system entities, schema version (`v4.0.0`), and key space mapping for administrative regions and OSINT parameters.

2. **Create Regional Registry (`data/regions.json`)**:
   - Establish integer primary key mapping for regional administrative units (e.g., ID 1..N with codes, names, H3 indices, and operational status).

3. **Create Territorial Passport Structure (`data/territories/` & sample passport)**:
   - Implement structured OSINT passport JSON schema (demographics, infrastructure, resources, P2P node density, risk vector $\vec{E}$).

4. **Implement Schema Validation Script (`scripts/validate_data_schema.py`)**:
   - Write a Python script that validates `data/manifest.json`, `data/regions.json`, and all `.json` files in `data/territories/` against structural constraints.

5. **Validation & Git Sync**:
   - Run `python scripts/validate_data_schema.py`.
   - Commit changes: `git commit -m "imperia_v4: Step B Database & OSINT Passports Framework complete"`.
   - Push to GitHub `main`.
   - Update `.v4_gateway/out/execution_state.json`.
