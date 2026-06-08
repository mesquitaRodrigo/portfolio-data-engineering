-- Calculate total revenue from all sales
-- Revenue = quantity * product price

SELECT 
    SUM(v.quantidade * p.preco) AS receita_total,
    COUNT(DISTINCT v.id_venda) AS total_vendas,
    COUNT(DISTINCT v.id_cliente) AS total_clientes,
    AVG(v.quantidade * p.preco) AS ticket_medio
FROM vendas v
JOIN produtos p ON v.id_produto = p.id_produto;
