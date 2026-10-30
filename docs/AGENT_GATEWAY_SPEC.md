# Imperia v4: Специфікація ШІ-Агентів та Шлюзів Баз Даних (Agent & Gateway Architecture)

## 1. Ієрархія ШІ-Агентів за Варнами
- **Брахман (Orchestrator / Gemini Notebook):** Приймач антропоморфного шуму, дистилятор інваріантів, хранитель контекстного поля (High Q >= 0.90). Взаємодіє з Supabase `brahman_knowledge_vault`.
- **Кшатрій (Executor / Cline):** Атомарний кодер, запевняч синтаксичної чистоти, виконавець директив, відповідальний за комміти та цілісність репозиторію.
- **Вайш'ї (Data Routers / P2P Swarm Nodes):** Провайдери ліквідності, маршрутизатори обчислювальних квантів, координатори локальних H3-кластерів.
- **Шудри (Peripheral Sensors / Edge Agents):** Джерела сирої гео-телеметрії, датчики стан-пам'яті H3 Res 9-12.

## 2. Шлюзи Даних (Data Gateways)
- **State Gateway (`docs/sl8_gateway.js`):** Забезпечує ізоляцію та синхронізацію між Master UI (`index.html`) та Kassator UI (`kassator.html`).
- **Supabase Vault Gateway (`docs/supabase_vault_client.js`):** Забезпечує читання/запис дистильованих інваріантів Брахмана у таблицю `brahman_knowledge_vault`.