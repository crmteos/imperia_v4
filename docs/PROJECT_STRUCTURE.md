# PROJECT STRUCTURE & STATE FILE SPECIFICATION (Imperia v4)

## 1. Карта Топології Інтерфейсів та Фізичних Файлів

### 1.1. Кореневий рівень (Root Infrastructure)
- `/STATE_GATEWAY_PROTOCOL.md` — Єдиний шлюз протоколів, онтологія Брахмана та індекс джерел.
- `/master_checklist.md` — Канонічний статусний чеклист та матриця контекстної міграції.
- `/.v4_gateway/` — Транспортний та архівний буфер (`in/`, `out/`, `archive/`).

### 1.2. Веб-інтерфейси (`/docs/`)
- `docs/index.html` — Master Sovereign UI (Головний монітор синархічної телеметрії, карти H3 та P2P-вузлів).
- `docs/kassator.html` — Kassator Executive Workbench (Операційний робочий стіл Касатора для керування ресурсами).
- `docs/map_core.html` — Standalone Map Core Engine (Ізольоване геопросторове ядро Leaflet + H3).

## 2. Специфікація Файлів Стан-Пам'яті (State Schemas)

### 2.1. Конфігурація та Телеметрія
- `docs/env_config.js` — Джерело конфігураційних змінних та API-ключів середовища.
- `docs/state_gateway.json` — Динамічний реєстр Q-факторів, статусу P2P-вузлів, вектора E та системних параметрів.
- `docs/h3_layers.json` — Геопросторова просторова сітка H3 (координати вузлів, Q-фактори, вектори E, шари symбіозу).

### 2.2. Географічні Паспорти Територій
- `docs/territory_passports.json` — Реєстр регіональних паспортів (Україна, Японія, глобальні хаби).
- `docs/japan_analysis.json` — Деталізований регіональний профіль Японії.

## 3. Модулі Логіки та Симуляції
- `docs/sl8_gateway.js` — Шлюз інтеграції із P2P-мережею Slate.
- `docs/p2p_simulator.js` — Симулятор топології та флуктуацій P2P-вузлів.

 Directory: c:\imperia_v4



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

#

- **Total files**: 23 (in docs directory)
- **Total directories**: 9 (root level)
- **Root directory**: c:\imperia_v4





