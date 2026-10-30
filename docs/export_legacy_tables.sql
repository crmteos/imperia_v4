-- Imperia v4: SQL-скрипт прямого вивантаження застарілих таблиць у JSON
-- Виконай кожен запит у Supabase SQL Editor і скопіюй результат у docs/legacy_archive/<table_name>.json

SELECT json_agg(t) FROM archivist_chronicles t;
SELECT json_agg(t) FROM futurology_forecasts t;
SELECT json_agg(t) FROM imperial_news t;
SELECT json_agg(t) FROM media_nodes t;
SELECT json_agg(t) FROM orchestra_knowledge t;
SELECT json_agg(t) FROM raw_sources t;
SELECT json_agg(t) FROM regions_register t;
SELECT json_agg(t) FROM secretary_chat_history t;
SELECT json_agg(t) FROM territory_passports t;
SELECT json_agg(t) FROM treasury_balances t;
SELECT json_agg(t) FROM vagon_ahtungs t;
SELECT json_agg(t) FROM worker_instructions t;
SELECT json_agg(t) FROM worldview_knowledge t;