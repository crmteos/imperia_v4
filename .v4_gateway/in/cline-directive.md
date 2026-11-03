# 1-Click Directive (Step 1): Audit, Invariant Extraction & Level 3 Role Separation

**Target Environment**: Local Repository `C:\imperia_v4`
**Issuer**: Level 2 Context Administrator (Gemini Notebook)
**Recipient**: Level 3 Role Engine (Cline in IDE)
**Target Action File**: `.v4_gateway\in\cline-directive.md`
**Execution Mode**: Step-by-Step Step 1 (Audit & Formal Role Separation)

---

## 1. EXECUTIVE PURPOSE & ARCHITECTURAL OBJECTIVE

This directive initiates **Step 1 of the Level 4 System Refactoring**.

The goal of this step is:

1. **Physical & Functional Separation of Level 3 Leadership Roles**: Split Level 3 responsibilities into two distinct, isolated roles:
   - **Role Architect (`02_architect.json`)**: Task decomposition, context mapping, sub-role allocation, and `execution_state.json` management.
   - **Role Administrator (`05_administrator.json`)**: Gateway file control (`in/`, `out/`), directory isolation enforcement, `STATE_CONTEXT_BRIDGE.md` compilation, pre-commit syntax validation, and Git version control.

2. **Context Audit & Invariant Extraction**: Audit all legacy/current documentation files and separate them into two clean canonical references:
   - **Level 2 Context Invariants** -> `.v4_gateway\in\context_invariants.md` (Rules governing Level 2 Context Engineering, 1-Click Relay, and Semantic Moderation).
   - **Level 3 Role Invariants** -> `.v4_gateway\roles\role_invariants.md` (Rules governing Level 3 Execution, Q-factor calculations, 4D vector $\vec{E}$, Atomic Commits, Hard Overwrite Rule).

---

## 🛠️ 2. PHASE 1: FORMALIZATION OF ROLE ADMINISTRATOR & ROLE ARCHITECT

### Action 1.1: Create Role Administrator Manifest

Create file `C:\imperia_v4\.v4_gateway\roles\manifests\05_administrator.json`:

```json
{
  "role_id": "05_administrator",
  "role_name": "Level 3 Role Administrator",
  "scope": "System Infrastructure, File Operations & Bridge Sync",
  "responsibilities": [
    "Manage .v4_gateway/in/ and .v4_gateway/out/ file streams",
    "Enforce physical file isolation rules (no loose HTML/JS scripts in root)",
    "Generate and update .v4_gateway/out/STATE_CONTEXT_BRIDGE.md after every step",
    "Perform pre-commit syntax control (node -c) on all modified JS assets",
    "Execute Git commits and maintain repository cleanliness"
  ],
  "allowed_tools": ["read_file", "write_file", "execute_command"],
  "prohibited_actions": [
    "Do not alter core UI business logic directly without Role Architect approval",
    "Do not delete source files permanently (archive only)"
  ]
}
```

### Action 1.2: Update Role Architect Manifest

Update file `C:\imperia_v4\.v4_gateway\roles\manifests\02_architect.json`:

```json
{
  "role_id": "02_architect",
  "role_name": "Level 3 Role Architect",
  "scope": "Local Task Decomposition & Role Orchestration",
  "responsibilities": [
    "Parse context manifests received from Level 2 in .v4_gateway/in/",
    "Decompose complex features into sub-tasks for Frontend, Diagnostician, and QA roles",
    "Maintain state tracking in .v4_gateway/roles/memory/execution_state.json",
    "Issue escalation tickets in bridge files when Level 2 context is missing"
  ],
  "allowed_tools": ["read_file", "write_file"],
  "prohibited_actions": [
    "Do not execute Git push operations directly (delegate to Role Administrator)",
    "Do not bypass physical file isolation rules"
  ]
}
```

---

## 🔍 3. PHASE 2: CONTEXT AUDIT & INVARIANT EXTRACTION

### Action 2.1: Extract Level 2 Context Invariants

Read `1.Єдиний_Фреймворк_Джерела_Правди_v3.0_Master_Framework.md` and `STATE_GATEWAY_PROTOCOL.md`. Extract all rules regarding Context Engineering, semantic moderation, and human-in-the-loop relay into:
`C:\imperia_v4\.v4_gateway\in\context_invariants.md`

*(This invariant file has already been created and contains the Level 2 Context Invariants.)*

### Action 2.2: Extract Level 3 Role Invariants

Read `ARCHITECTURE_DECISIONS.md`, `1.Єдиний_Фреймворк...`, and `master_checklist.md`. Extract all formulas ($Q$-factor, vector $\vec{E}$), node coherence bounds ($Q \ge 0.85$), Leaflet/H3 tile constraints, Hard Overwrite rules, and pre-commit protocols into:
`C:\imperia_v4\.v4_gateway\roles\role_invariants.md`

---

## 📊 4. PHASE 3: BRIDGE SYNC & TELEMETRY DUMP

### Action 3.1: Generate `STATE_CONTEXT_BRIDGE.md`

**Role Administrator** must compile and write the state snapshot to:
`C:\imperia_v4\.v4_gateway\out\STATE_CONTEXT_BRIDGE.md`

#### Required Markdown Structure:

```markdown
# STATE CONTEXT BRIDGE SNAPSHOT

## 1. System Status & Level 3 Role Allocation
- **Role Architect Status**: Active (Decomposition & State Memory initialized)
- **Role Administrator Status**: Active (Gateway & Syntax Control active)
- **Active Manifests**: 01_diagnostician, 02_architect, 03_frontend_dev, 04_qa_engineer, 05_administrator

## 2. Invariants Extraction Summary
- Level 2 Context Invariants: Extracted to `.v4_gateway/in/context_invariants.md` [OK]
- Level 3 Role Invariants: Extracted to `.v4_gateway/roles/role_invariants.md` [OK]

## 3. Physical Directory Audit
- Root directory clean: Yes
- Web assets isolated in `docs/`: Yes
- Archived legacy assets in `/.v4_gateway/archive/`: Confirmed

## 4. Pending Escalations / Questions for Level 2
- Escalations: None. Ready for Step 2 Refactoring.
```

### Action 3.2: Git Commit & Push

Run terminal commands:

```bash
git add .v4_gateway/ master_checklist.md
git commit -m "refactor(level3): separate Role Architect/Admin and extract v4 invariants (Step 1)"
git push origin main
```

---

## ✅ COMPLETION VERIFICATION FOR CLINE

Upon execution, Cline must log:

1. Manifest `05_administrator.json` created.
2. Invariants files `context_invariants.md` and `role_invariants.md` written.
3. Bridge file `STATE_CONTEXT_BRIDGE.md` generated in `.v4_gateway/out/`.
4. Git commit and push confirmed.