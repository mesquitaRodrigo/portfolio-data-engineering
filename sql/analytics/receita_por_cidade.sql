-- Calculate revenue by city
-- This query reads from the Curated Layer (data/curated/)
-- Shows total revenue per city with customer count

SELECT 
    dc.cidade,
    SUM(f.valor_total) AS receita_total
FROM read_parquet('data/curated/fato_vendas.parquet') f
INNER JOIN read_parquet('data/curated/dim_cliente.parquet') dc ON f.id_cliente = dc.id_cliente
GROUP BY dc.cidade
ORDER BY receita_total DESC;
