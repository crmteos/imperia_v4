# DIRECTIVE: STEP 3 - CODEBASE REFACTORED ALIGNMENT & UI ISOLATION (Imperia v4)

**Role**: Local System Engineer (Cline)  
**Execution Context**: Level 3 (Role Architect `02_architect` & Role Administrator `05_administrator`)  
**Target Directory**: `C:\imperia_v4\`  
**Target Protocol**: 3-Level Architecture Protocol / Context Engineering v3.0  

---

## 📍 1. OBJECTIVE & CONSTRAINTS

Step 1 (Invariants Audit) and Step 2 (Role Manifests & Bridge Setup) are complete.  
**Step 3 Focus**: Finalize the physical code alignment of `docs/` and repository assets with the v4.0 canonical architecture.

### 🛡️ Mandatory Execution Constraints:
1. **Physical UI Isolation Invariant**:
   * `docs/index.html` (Master Sovereign UI) MUST remain completely isolated from `docs/kassator.html` (Tenant UI).
   * Cross-ui communication MUST occur via the `docs/sl8_gateway.js` event bus.
2. **CSS Protection**:
   * `docs/style.css` must maintain Leaflet tile fix: `.leaflet-container img { max-width: none !important; }`.
3. **Hard Overwrite Rule**:
   * Fully overwrite files when making structural updates; do not leave trailing partial snippets.
4. **Pre-Commit Syntax & Git Execution**:
   * Validate JS files with `node -c`.
   * Update `STATE_CONTEXT_BRIDGE.md` and `master_checklist.md`.
   * Commit and push to `origin main`.

---

## 🛠️ 2. STEP 3 TASK BREAKDOWN

### Task 3.1: Clean & Validate `docs/` Workspace
* Ensure no stray temporary (`*.tmp`, `*.bak`, `*.recovered`) files remain in `docs/`.
* Verify that core web scripts are properly referenced:
  - `docs/sl8_gateway.js`
  - `docs/p2p_simulator.js`
  - `docs/poc_reward_engine.js`
  - `docs/territory_passports.json`

### Task 3.2: Role Administrator Telemetry & Checklist Update
* Update `master_checklist.md` to reflect full 3-Level Architecture Readiness & Refactoring completion.
* Update `/.v4_gateway/out/STATE_CONTEXT_BRIDGE.md` with:
  - Current timestamp
  - Active role statuses
  - Clean git status confirmation

### Task 3.3: Pre-Commit Syntax Validation & Git Push
Execute in CLI:
```bash
node -c docs/sl8_gateway.js
node -c docs/p2p_simulator.js
node -c docs/poc_reward_engine.js

git add .
git commit -m "refactor(v4.0): finalize codebase refactoring and UI isolation under 3-Level Protocol"
git push origin main
```

---

## ✅ COMPLETION VERIFICATION

Upon finishing, generate the updated `/.v4_gateway/out/STATE_CONTEXT_BRIDGE.md` and print a summary log confirming:
1. Syntax validation passed (`node -c`).
2. Clean `git push` status.
3. System ready for Phase 8 execution.
