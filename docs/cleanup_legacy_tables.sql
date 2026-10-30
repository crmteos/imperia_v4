-- Imperia v4: SQL-скрипт очищення активної БД Supabase від застарілих таблиць
-- УВАГА: Виконувати ТІЛЬКИ після збереження заготовок у docs/legacy_archive/

DROP TABLE IF EXISTS archivist_chronicles CASCADE;
DROP TABLE IF EXISTS futurology_forecasts CASCADE;
DROP TABLE IF EXISTS imperial_news CASCADE;
DROP TABLE IF EXISTS media_nodes CASCADE;
DROP TABLE IF EXISTS orchestra_knowledge CASCADE;
DROP TABLE IF EXISTS raw_sources CASCADE;
DROP TABLE IF EXISTS regions_register CASCADE;
DROP TABLE IF EXISTS secretary_chat_history CASCADE;
DROP TABLE IF EXISTS territory_passports CASCADE;
DROP TABLE IF EXISTS treasury_balances CASCADE;
DROP TABLE IF EXISTS vagon_ahtungs CASCADE;
DROP TABLE IF EXISTS worker_instructions CASCADE;
DROP TABLE IF EXISTS worldview_knowledge CASCADE;

-- Перевірка залишкових таблиць (повинна залишитися тільки brahman_knowledge_vault)
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';