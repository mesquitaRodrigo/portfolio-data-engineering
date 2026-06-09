-- Extract script for clientes table from ERP (PostgreSQL)
-- This query extracts all customer data without transformation
-- Used to populate the Raw Layer (data/raw/clientes.parquet)

SELECT 
    id,
    nome,
    cidade,
    email,
    telefone,
    data_cadastro,
    ativo,
    NOW() as extract_timestamp
FROM clientes
WHERE ativo = TRUE;
