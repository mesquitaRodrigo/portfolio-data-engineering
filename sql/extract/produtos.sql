-- Extract script for produtos table from ERP (PostgreSQL)
-- This query extracts all product data without transformation
-- Used to populate the Raw Layer (data/raw/produtos.parquet)

SELECT 
    id_produto,
    nome,
    categoria,
    preco,
    estoque,
    data_cadastro,
    ativo,
    NOW() as extract_timestamp
FROM produtos
WHERE ativo = TRUE;
