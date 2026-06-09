-- Calculate revenue by product
-- This query reads from the Curated Layer (data/curated/)
-- Shows total revenue per product with product details

SELECT 
    dp.nome AS produto,
    SUM(f.valor_total) AS receita_total
FROM read_parquet('data/curated/fato_vendas.parquet') f
INNER JOIN read_parquet('data/curated/dim_produto.parquet') dp ON f.id_produto = dp.id_produto
GROUP BY dp.nome
ORDER BY receita_total DESC;
