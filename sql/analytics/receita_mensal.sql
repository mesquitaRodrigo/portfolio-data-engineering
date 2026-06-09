-- Monthly revenue
-- This query reads from the Curated Layer (data/curated/)
-- Shows revenue by year and month using dim_data

SELECT 
    dd.ano,
    dd.mes,
    dd.nome_mes,
    SUM(f.valor_total) AS receita_total
FROM read_parquet('data/curated/fato_vendas.parquet') f
INNER JOIN read_parquet('data/curated/dim_data.parquet') dd ON f.data_pedido = dd.data
GROUP BY dd.ano, dd.mes, dd.nome_mes
ORDER BY dd.ano, dd.mes;
