-- Top 5 clients by revenue
-- This query reads from the Curated Layer (data/curated/)
-- Shows top 5 clients by total revenue

SELECT 
    dc.nome AS cliente,
    SUM(f.valor_total) AS receita_total
FROM read_parquet('data/curated/fato_vendas.parquet') f
INNER JOIN read_parquet('data/curated/dim_cliente.parquet') dc ON f.id_cliente = dc.id_cliente
GROUP BY dc.nome
ORDER BY receita_total DESC
LIMIT 5;
