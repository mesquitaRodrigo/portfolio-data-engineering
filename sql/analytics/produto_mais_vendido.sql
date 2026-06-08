-- Find the most sold product by quantity
-- Shows product details with total quantity sold and revenue

SELECT 
    p.id_produto,
    p.nome AS nome_produto,
    p.categoria,
    p.preco,
    SUM(v.quantidade) AS quantidade_total_vendida,
    COUNT(v.id_venda) AS numero_vendas,
    SUM(v.quantidade * p.preco) AS receita_total
FROM vendas v
JOIN produtos p ON v.id_produto = p.id_produto
GROUP BY p.id_produto, p.nome, p.categoria, p.preco
ORDER BY quantidade_total_vendida DESC
LIMIT 1;
