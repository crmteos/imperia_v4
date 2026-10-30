-- Imperia v4: Brahman Sovereign Knowledge Vault Schema (Supabase)
-- Призначення: Фізичне векторно-контекстне сховище інваріантів Брахмана

CREATE TABLE IF NOT EXISTS brahman_knowledge_vault (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    m_octave VARCHAR(10) NOT NULL, -- Код октави: M0, M1, M2, M3, M4, M5, M6
    domain_category VARCHAR(50) NOT NULL, -- 'ontology', 'wave_physics', 'synarchy', 'user_vision', 'territory_passports'
    raw_signal TEXT NOT NULL, -- Первинний антропоморфний потік / текст першоджерела
    distilled_invariant TEXT NOT NULL, -- Очищений канонічний інваріант / формула / алгоритм
    q_coherence_score NUMERIC(3,2) DEFAULT 0.95, -- Рівень добротності знання (0.00 - 1.00)
    tags TEXT[], -- Масив тегів ['shmakov', 'h3', 'vector_E', 'q_factor', 'living_tree']
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Індекси для прискорення кешованого зчитування
CREATE INDEX IF NOT EXISTS idx_brahman_vault_octave ON brahman_knowledge_vault(m_octave, domain_category);