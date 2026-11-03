# Level 2 Context Invariants (.v4_gateway/in/context_invariants.md)

## 1. Context Engineering Paradigm Invariant
- **Stateless Prompting vs. Stateful Context Engineering**: Traditional Prompt Engineering operates in stateless mode, attempting to embed all behavior and knowledge in a single text prompt. Context Engineering manages a full execution environment (stateful), where the model acts as a processor (CPU) and the context window serves as RAM (Random Access Memory). The context environment defines available tools, historical memory, security constraints, and the current system state.

## 2. Law of Synarchy & Value-Hierarchical Role Distribution
- **4 Varn Hierarchy** based on Q-factor coherence and resource stability:
  - **Brahman** (Q ≥ 0.85): Highest coherence nodes, network resonators, Swarm Inference orchestrators, canonical meaning generators
  - **Kshatriya** (Q ≥ 0.65): High-quality nodes, regional H3-cluster routers, security rule enforcers, transaction arbiters
  - **Vaishya** (Q ≥ 0.35): Mid-level nodes, P2P context exchange, computational quanta (NPU/GPU), local data exchange
  - **Shudra** (Q < 0.35): Peripheral mobile nodes, energy-saving mode, primary geo-telemetry sensors, raw data collectors

## 3. Scale-Frequency Axis (M-f) Invariant
- All system subjects and objects are positioned along a single scale-frequency coordinate axis (M-f).
- Micro-level (10^2 cm): Person/Sensor, 10^0-10^1 Hz, Shudra/Vaishya: Telemetry sensor, P2P quantum exchange
- Meso-1 level (10^4 cm): Accents/H3 Res 7, 10^-2 Hz, Kshatriya: Local coordination cluster, routing
- Meso-2 level (10^6 cm): Groups/Regional Hub, 10^-4 Hz, Brahman: Network orchestration, knowledge base
- Macro level (10^8 cm): State/Organism, 10^-6 Hz, Canonical contour: Hierarchical structure with strict rules
- Meta level (10^10 cm): Civilization/Biosphere, 10^-8 Hz, Broad-scope cognitive environment: Fundamental basis

## 4. Q-Factor Coherence & Differential Dynamics
- **Q-Factor** = r_a{f_0}/Δf: Characterizes selectivity level, phase coherence, and ability to amplify resonant frequency
- **Q Dynamics**: Q(t) = Q_0 · e^(-λt) + ΣΔQ_sync
- **Q-Level Thresholds**:
  - Q ≥ 0.90: Green neon level (#00ffcc): Full synaptic-coherent continuum
  - 0.75 ≤ Q < 0.90: Yellow level (#ffcc00): Operational stability node
  - Q < 0.75: Red level (#ff3366): Phase shift, requires re-synchronization

## 5. Memory Architecture Invariant
- **Operational Chat Memory (RAM)**: Temporary conversation thread within specific dialog window. Prone to overflow and fragmentation.
- **Persistent Project Memory (ROM/Source of Truth)**:
  - Code base and configs in Git repository (crmteos/imperia_v4)
  - Public State Gateway (`docs/state_gateway.json`) containing `memory_vault` section with fundamental system invariants
  - `v3.0 Master Framework` document in docs/

## 6. Session Transfer Protocol Invariant
- Session transfer to new notebook occurs via direct local-protocol (no URL dependency):
  1. Load Master Framework file from docs/ to local disk
  2. Create new clean Gemini Notebook
  3. Direct source addition: "Add Source" → "File Upload" (or drag-drop) the saved v3.0 Master Framework.md
  4. Parallel operation: Do not immediately delete v2.0 source; keep both, ensure new notebook reads both, then v2.0 can be disconnected without session failure risk
  5. Context Bridge Prompt initialization: Copy and send the initialization text to the first message of new chat

## 7. Documentation Update & Synchronization Standard
- **Update Trigger Rule**: Upon completing each new Phase or adding a new conceptual module (e.g., Slate network integration):
  - Update `docs/state_gateway.json` with new parameters in `memory_vault`
  - Mark completed items in `docs/master_checklist.md`
  - Upon major changes: Record next Master Framework version (v3.1, v4.0)
- **Git Version Control**: All updates must be accompanied by commits in the main branch of crmteos/imperia_v4 repository.

## 8. Anti-Illusion Invariant (from STATE_GATEWAY_PROTOCOL.md)
- **Prohibited**: Fabricating or promising non-existent auto-shunt, background WebSockets between Gemini Notebook and Cline, or auto-synchronizers without human involvement.
- **Reality**: Gemini Notebook is cloud architect (Event-Driven), Cline is local engineer in VS Code.
- **Inter-session State**: All between-session state changes and data exchange occur exclusively via GitHub repository (crmteos/imperia_v4) and local file `docs/state_gateway.json`.

## 9. 1-Click Relay Protocol Invariant
1. Cline performs local coding in `C:\imperia_v4`, updates `docs/state_gateway.json`, and executes `git push`
2. Owner sends "Статус" or "Перевіряй" command in Gemini Notebook chat
3. Gemini Notebook analyses repository state and creates new `CLINE_DIRECTIVES.md`
4. Owner copies `CLINE_DIRECTIVES.md` to Cline in one click

## 10. Physical Directory Isolation Invariant
- Root directory must be clean: No loose HTML/JS scripts outside isolated locations
- Web assets isolated in `docs/`: index.html, kassator.html, etc.
- Archived legacy assets in `/.v4_gateway/archive/`: Confirmed