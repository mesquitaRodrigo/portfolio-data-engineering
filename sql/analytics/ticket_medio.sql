-- Calculate average ticket (average sale value)
-- This query reads from the Curated Layer (data/curated/)
-- Shows overall average ticket

SELECT 
    AVG(f.valor_total) AS ticket_medio
FROM read_parquet('data/curated/fato_vendas.parquet') f;
