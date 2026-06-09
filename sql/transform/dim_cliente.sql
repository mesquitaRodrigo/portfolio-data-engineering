-- Transform script to create dim_cliente from Raw Layer
-- This query transforms raw customer data into a dimensional model
-- Used to populate the Curated Layer (data/curated/dim_cliente.parquet)

-- Note: This SQL is designed to work with DuckDB on Parquet files
-- Replace 'data/raw/' with actual path to raw layer

SELECT 
    id as sk_cliente,
    id as nk_cliente,
    nome,
    cidade,
    email,
    telefone,
    data_cadastro,
    ativo,
    extract_timestamp,
    CURRENT_TIMESTAMP as dw_load_timestamp
FROM read_parquet('data/raw/clientes.parquet')
WHERE ativo = TRUE;
