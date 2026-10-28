# Imperia v4 Project Structure
## Generated: 2026-10-28
## Root Directory: c:\imperia_v4

### Directory Tree

```
.
├── .clinerules                  (configuration file)
├── .pytest_cache/               (test cache)
├── .v4_gateway/                 (gateway engine)
├── build_app.js                  (build script)
├── config/                      (configuration files)
├── copy_modules.py              (utility script)
├── copy_swarm.py                (utility script)
├── create_all_modules.py        (module creator)
├── create_h3.py                 (H3 geo-matrix creator)
├── create_modules.py            (module creator)
├── data/                        (data directory)
├── debug_transport.py           (debug utility)
├── docs/                        (documentation)
│   ├── 1. Єдиний Фреймворк Джерела Правди v3.0 Master Framework.md
│   ├── 2. Зведений Реєстр Документації, Дорожня Карта та Специфікація Стан-Пам'яті Проєкту (Imperia v4, v3.0 Master Release).md
│   ├── 3. master_checklist.md
│   ├── 4. Специфікація та Співвідношення Парадигм_ Рольове, Антропоморфне та Контекстне Програмування (Context Engineering v3.0).md
│   ├── app.js
│   ├── app.js.bak
│   ├── index.html               (IMPERIA v4: Master Sovereign UI - Spec v3.0)
│   ├── index.html.bak
│   ├── japan_analysis.json
│   ├── kassator.html
│   ├── master_checklist.md
│   ├── negotiator_agent.js
│   ├── p2p_simulator.js
│   ├── poc_reward_engine.js
│   ├── sl8_gateway.js           (Multi-Tenant Gateway Engine)
│   ├── state_gateway.json       (Session state persistence)
│   ├── style.css
│   ├── telegram_bot.js
│   ├── telemetry_engine.js
│   ├── telemetry_feed.json
│   ├── territory_passports.json
│   ├── tz-slate-integration-v3.md  (Specification v3.0)
│   └── style.css
├── scripts/                     (utility scripts)
│   └── build_catalog.js         (directory indexer script)
├── src/                         (source code)
├── tests/                       (test suite)
├── 📄 *.py                      (various Python scripts)
├── *.md                         (project documentation)
├── *.docx                       (project concept)
└── package.json                (project dependencies)
```

### File Count Summary

- **Total files**: 23 (in docs directory)
- **Total directories**: 9 (root level)
- **Root directory**: c:\imperia_v4
- **Ignored**: node_modules, .git
- **Last generated**: 2026-10-28

### Key Files Description

- `index.html` - Master Sovereign UI with Leaflet map, 3-tier filters, regional passports
- `kassator.html` - Kassator Telemetry UI (separate module, do not merge with index.html)
- `sl8_gateway.js` - Multi-Tenant Gateway Engine
- `state_gateway.json` - Session state persistence across sessions
- `master_checklist.md` - Master override status and audit logs
- `tz-slate-integration-v3.md` - Specification v3.0 compliance reference
- `.clinerules` - Cline invariants for consistent AI-assisted development