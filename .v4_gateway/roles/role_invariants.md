# Level 3 Role Invariants (.v4_gateway/roles/role_invariants.md)

## 1. Universal Wave Model & Vector Field E
- **4D Vector Field**: $\vec{E} = [E_{lang}, E_{geo}, E_{hist}, E_{soc}]^T$
- **Effective Field Power**: $P_{eff} = \|\vec{E}\| \times Q$

## 2. Q-Factor Coherence Dynamics
- **Q-Factor Dynamics**: $Q(t) = Q_0 \cdot e^{-\lambda t} + \sum \Delta Q_{sync}$
- **Q-Level Thresholds**:
  - Q ≥ 0.90: Green neon level (#00ffcc): Full synarchic & phase-coherent continuum
  - 0.75 ≤ Q < 0.90: Yellow level (#ffcc00): Operational stability node
  - Q < 0.75: Red level (#ff3366): Phase desynchronization, requires resonant re-loading

## 3. Scale-Frequency Axis (M-f) & Living Tree Principle
- **7-Level M-Axis Matrix** with H3 Resolutions:
  - M₀ (Sub-Edge): H3 Res 15-12, NPU/GPU chip, IoT sensor, hardware module - Periphery (Shudra-Kirta): Raw ge telemetry reading, local tick generator
  - M₁ (Micro-Personal): H3 Res 11-10, Personal device, person, mobile agent - Shudra/Vaishya: P2P calculation quanta (Resource Pooling), TELEMETRY_STREAM transfer
  - M₂ (Meso-0/Oseredok): H3 Res 9 (~0.1 km²), Local focus, house, P2P neighborhood - Vaishya/Kshatriya: Local P2P node discovery (libp2p, WebRTC, Kademlia DHT), context exchange
  - M₃ (Meso-1/City District): H3 Res 8-7 (~5.2 km²), City district, micro-hub - Kshatriya: H3-cluster routing, security control, frequency coordination (Q ≥ 0.65)
  - M₄ (Meso-2/Regional Hub): H3 Res 6-4 (~11,000 km²), Regional contour, Cathedral Hub (Kyiv, Lviv) - Brahman: Swarm Inference orchestration, knowledge base coordination (Q ≥ 0.85)
  - M₅ (Macro/State Contour): H3 Res 3-1 (~1,000,000 km²), Nation, sovereign state contour (Ukraine) - Canonical Contour (Master UI): Owner's sovereign oversight, legal & conceptual invariants
  - M₆ (Meta/Biosphere Mesh): H3 Res 0 (~4,250,000 km²), Planetary P2P mesh, Noosphere - Broad-scale synchronizer, fundamental coherence attraction

- **Living Tree Principle**: The canonical 7-level M-axis matrix is NOT a statistically fixed "dead canon". It is a fractal living structure: any octave can be additionally detailed or expanded into sub-octaves (sub-octave branching) without violating system phase coherence.

## 4. Calibration Metrics Invariant
- **Synchronicity Index ($I_{syn}$)**: Balance between H3-node autonomy (differentiation) and ability to cohesive synthesis (integration)
- **Hierarchical Correspondence Coefficient ($A_{hier}$)**: Purity of Varn role execution according to computational coherence Q
- **Adaptability Plasticity Index ($K_{evol}$)**: Object capacity for dynamic sub-octave branching under the "Living Tree" principle
- **Traditional State Vector ($\vec{T}$)**:
  - `spirit_identity`: Ideological-contextual purity & meaning coherence
  - `form_structure`: Code base quality, DOM integrity, H3-sheet integrity
  - `energy_resource`: Hardware computational quantum (NPU/GPU, RAM, bandwidth)

## 5. Two-Contour Tokenomics Invariant
- **Inner Contour**: Null-budget, resource pooling among devices
- **Outer Contour**: SSLX/Slate token for cross-border calculations
- **H3 Geospatial Indexing**: Uber H3 usage for P2P-node localization and Sovereign Synergies

## 6. Role-Specific Invariants

### Role Architect (02_architect) Invariants
- Task decomposition & context mapping
- Sub-role allocation and `execution_state.json` management
- Schema design and spec writing
- **Prohibited**: Direct UI coding without Role Architect approval; Bypassing physical file isolation rules

### Role Administrator (05_administrator) Invariants
- `.v4_gateway/in/` and `.v4_gateway/out/` file stream management
- Physical file isolation rule enforcement (no loose HTML/JS scripts in root)
- `STATE_CONTEXT_BRIDGE.md` generation & update after every step
- Pre-commit syntax control (node -c) on all modified JS assets
- Git commits and repository cleanliness maintenance
- **Prohibited**: Altering core UI business logic directly without Role Architect approval; Permanent deletion of source files (archive only)

### Role Diagnostician (01_diagnostician) Invariants
- Read file, list dir, syntax check, log telemetry
- Input sources: `.v4_gateway/out/STATE_GATEWAY_TELEMETRY.md`, `docs/`
- Output target: `.v4_gateway/roles/memory/execution_state.json`
- **Prohibited**: Modify production code

### Role Frontend Developer (03_frontend_dev) Invariants
- UI isolation v3.0: `docs/index.html` vs `docs/kassator.html` separation
- Leaflet 1.9.4 from Cloudflare CDN with Ukrainian language (lang="uk")
- 3-tier filter dropdowns (country → region → module)
- Full-width Leaflet map as dominant visual center
- Regional passport rows with 4D ecology vectors E = [E_lang, E_geo, E_hist, E_soc]^T
- H3 geo-matrix module options
- Master override control buttons with proper alert messages
- Kassator UI linking

### Role QA Engineer (04_qa_engineer) Invariants
- Q-factor coherence validation (Q ≥ threshold checks)
- Pre-commit syntax checks (node -c)
- Git cleanliness enforcement
- Hard overwrite rule enforcement
- Audit log maintenance