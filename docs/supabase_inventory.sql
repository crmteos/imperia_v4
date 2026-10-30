-- Imperia v4: Supabase Schema Read-Only Inventory Script
-- Призначення: Безпечна інвентаризація всіх таблиць public-схеми для подальшої дистиляції та чистки

SELECT 
    t.table_name,
    pg_size_pretty(pg_total_relation_size('"' || t.table_schema || '"."' || t.table_name || '"')) AS total_size,
    (SELECT COUNT(*) FROM information_schema.columns c WHERE c.table_name = t.table_name AND c.table_schema = t.table_schema) AS column_count
FROM 
    information_schema.tables t
WHERE 
    t.table_schema = 'public'
    AND t.table_type = 'BASE TABLE'
ORDER BY 
    t.table_name;