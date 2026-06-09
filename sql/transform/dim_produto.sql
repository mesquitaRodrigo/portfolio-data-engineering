-- Transform script to create dim_produto from Raw Layer
-- This query transforms raw product data into a dimensional model
-- Used to populate the Curated Layer (data/curated/dim_produto.parquet)

-- Note: This SQL is designed to work with DuckDB on Parquet files
-- Replace 'data/raw/' with actual path to raw layer

SELECT 
    id_produto as sk_produto,
    id_produto as nk_produto,
    nome,
    categoria,
    preco,
    estoque,
    data_cadastro,
    ativo,
    extract_timestamp,
    CURRENT_TIMESTAMP as dw_load_timestamp
FROM read_parquet('data/raw/produtos.parquet')
WHERE ativo = TRUE;
