-- Imperia v4: Supabase Spatial Vector Schema
CREATE EXTENSION IF NOT EXISTS vector;

-- Таблиця H3 Геопросторових Осередків
CREATE TABLE IF NOT EXISTS h3_spatial_cells (
    cell_id VARCHAR(64) PRIMARY KEY, -- H3 Index (Res 4 / 7 / 9)
    region_name VARCHAR(128),
    coordinates POINT,
    q_factor NUMERIC(4,3) DEFAULT 0.850,
    vector_e vector(4), -- 4D Vector [E_lang, E_geo, E_hist, E_soc]
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Таблиця Макроорганізмів та Геопаспортів
CREATE TABLE IF NOT EXISTS macro_symbiosis_registry (
    id VARCHAR(64) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    symbiosis_type VARCHAR(64), -- Church+State, Language Egregores, Sl8 Nodes
    h3_cell_id VARCHAR(64) REFERENCES h3_spatial_cells(cell_id),
    pattern_vector vector(4),
    q_factor NUMERIC(4,3),
    metadata JSONB DEFAULT '{}'::jsonb
);