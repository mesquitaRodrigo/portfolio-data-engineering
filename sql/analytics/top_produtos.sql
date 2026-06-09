-- Top 5 products by quantity sold
-- This query reads from the Curated Layer (data/curated/)
-- Shows top 5 products by total quantity sold

SELECT 
    dp.nome AS produto,
    SUM(f.quantidade) AS quantidade_total
FROM read_parquet('data/curated/fato_vendas.parquet') f
INNER JOIN read_parquet('data/curated/dim_produto.parquet') dp ON f.id_produto = dp.id_produto
GROUP BY dp.nome
ORDER BY quantidade_total DESC
LIMIT 5;
