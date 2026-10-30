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

### 2.3. Канонічні JSON-шаблони записів стан-пам'яті

Нижче надано єдиний канонічний шаблон запису, який використовується одночасно для `docs/territory_passports.json` та `docs/h3_layers.json`. Кожен об'єкт у цих файлах має дотримуватися наступної структури:

```json
{
  "entity_id": "UA-KYIV-M4",
  "name": "Київський Соборний Хаб",
  "m_axis": {
    "octave_code": "M4",
    "scale_name": "Meso-2: Regional Hub",
    "h3_resolution": 4,
    "spatial_index_h3": "872b101ffffff",
    "nesting_factor_K": 7
  },
  "vector_E": {
    "lang": 0.95,
    "geo": 0.91,
    "hist": 0.98,
    "soc": 0.89,
    "E_norm": 0.932
  },
  "coherence_Q": {
    "current_Q": 0.94,
    "status_band": "GREEN"
  },
  "synarchy_metrics": {
    "cohesion_index_Isyn": 0.92,
    "hierarchical_alignment_Ahier": 0.96,
    "evolutionary_plasticity_Kevol": 0.88,
    "triadic_state": {
      "spirit_identity": 0.95,
      "form_structure": 0.92,
      "energy_resource": 0.89
    }
  },
  "field_power_Peff": 0.876,
  "synarchy_role": "Brahman"
}
```

**Поля шаблону:**

| Поле | Тип | Опис |
| :--- | :--- | :--- |
| `entity_id` | `string` | Унікальний ідентифікатор сутності у форматі `<КодКраїни>-<Місто/Регіон>-<Октава>`. |
| `name` | `string` | Назва об'єкта на українській мові. |
| `m_axis.octave_code` | `string` | Код октави M-осі: `M0` … `M6`. |
| `m_axis.scale_name` | `string` | Назва рівня масштабу (наприклад, "Meso-2: Regional Hub"). |
| `m_axis.h3_resolution` | `integer` | Uber H3 разрешальна здатність (0–15). |
| `m_axis.spatial_index_h3` | `string` | H3-індекс геосектора (16-знаковий геeksadecimal). |
| `m_axis.nesting_factor_K` | `integer` | Коефіцієнт гніздящості/вкладеності (канонічно 7). |
| `vector_E.lang` | `number` (0.0–1.0) | Мовно-культурний коефіцієнт когерентності. |
| `vector_E.geo` | `number` (0.0–1.0) | Геопросторова прив'язка H3 (просторова щільність). |
| `vector_E.hist` | `number` (0.0–1.0) | Історико-хронологічна спадкоємність. |
| `vector_E.soc` | `number` (0.0–1.0) | Соціально-синархічний коефіцієнт довіри. |
| `vector_E.E_norm` | `number` (0.0–1.0) | Нормалізована довжина 4D-вектора \\(\\|\vec{E}\\|\\). |
| `coherence_Q.current_Q` | `number` (0.00–1.00) | Поточний рівень фазової когерентності. |
| `coherence_Q.status_band` | `string` | Статусний діапазон: `GREEN` (\\(Q \\ge 0.90\\)), `YELLOW` (\\(0.75 \\le Q < 0.90\\)), `RED` (\\(Q < 0.75\\)). |
| `field_power_Peff` | `number` (0.0–1.0) | Ефективна потужність поля: \\(P_{eff} = \\|\vec{E}\\| \\times Q\\). |
| `synarchy_metrics.cohesion_index_Isyn` | `number` (0.0–1.0) | Індекс синархічної когезії — баланс автономії вузла та здатності до соборного синтезу. |
| `synarchy_metrics.hierarchical_alignment_Ahier` | `number` (0.0–1.0) | Коефіцієнт ієрархічної відповідності — чистота виконання Варнової ролі відповідно до Q. |
| `synarchy_metrics.evolutionary_plasticity_Kevol` | `number` (0.0–1.0) | Індекс адаптивної пластичності — здатність до динамічного розгалуження під-октав. |
| `synarchy_metrics.triadic_state.spirit_identity` | `number` (0.0–1.0) | Ідейно-контекстна чистота та когерентність смислів. |
| `synarchy_metrics.triadic_state.form_structure` | `number` (0.0–1.0) | Якість кодової бази, цілісність DOM та H3-сітки. |
| `synarchy_metrics.triadic_state.energy_resource` | `number` (0.0–1.0) | Апаратний обчислювальний квант (NPU/GPU, RAM, bandwidth). |
| `synarchy_role` | `string` | Вартова роль сутності (наприклад, `Brahman`, `Kshatriya`, `Vaishya`, `Shudra`, `Periphery`). |

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





