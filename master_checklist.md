# MASTER CHECKLIST & CONTEXT MIGRATION ROADMAP (Imperia v4)

## 1. Реєстр Канонічних Джерел Проєкту
- [x] `/STATE_GATEWAY_PROTOCOL.md` — Шлюз взаємодії та онтологія Брахмана
- [/] `/master_checklist.md` — Єдиний дорожній чеклист та таблиця міграції
- [ ] `/docs/ARCHITECTURE_DECISIONS.md` — Зведена математика, Q-динаміка та вектор E
- [ ] `/docs/PROJECT_STRUCTURE.md` — Карта коду, DOM-компоненти та JSON-схем

## 2. Матриця Аудиту та Перенесення Контексту (Context Audit)
Завдання: Перенести 100% унікальних даних у канонічні файли перед архівуванням у /.v4_gateway/archive/

| Вхідний файл для аудиту | Цільовий канонічний файл | Статус витягу контексту | Статус переміщення у archive/ |
| :--- | :--- | :---: | :---: |
| `docs/3.master_checklist.md` | `/master_checklist.md` | [x] Витягнуто | [x] Перенесно до archive/ |
| `docs/STATE_GATEWAY_PROTOCOL.md` | `/STATE_GATEWAY_PROTOCOL.md` | [x] Витягнуто | [x] Перенесно до archive/ |
| `docs/master_checklist.md` | `/master_checklist.md` | [x] Витягнуто | [x] Перенесно до archive/ |
| Усі тимчасові файли `update_*.md` з кореня | `/docs/ARCHITECTURE_DECISIONS.md` | [x] Витягнуто | [ ] Ні |
| JSON/JS файли в корені та .v4_gateway | `/docs/PROJECT_STRUCTURE.md` | [x] Витягнуто | [ ] Ні |

## 3. Статус Технічних Фаз Розробки
- [x] Фаза 0: Базовий дашборд та Телеметрія Q = 0.94
- [x] Фаза 0.5: H3 Spatial Grid та Leaflet Map Engine (CartoDB/OSM)
- [x] Фаза 1: Декомпозиція UI v3.0 (Master UI index.html / Kassator UI kassator.html)
- [ ] Фаза 2: Тотальне наповнення H3-паспортів (territory_passports.json та japan_analysis.json)
- [ ] Фаза 3: P2P Topology Simulator (p2p_simulator.js)
- [ ] Фаза 4: Telegram Channel Gateway (@imperial_chancery)