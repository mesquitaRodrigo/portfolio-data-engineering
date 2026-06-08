-- Calculate revenue by client
-- Shows total revenue per client with client details

SELECT 
    c.id AS id_cliente,
    c.nome AS nome_cliente,
    c.cidade,
    SUM(v.quantidade * p.preco) AS receita_total,
    COUNT(v.id_venda) AS total_vendas,
    AVG(v.quantidade * p.preco) AS ticket_medio
FROM vendas v
JOIN clientes c ON v.id_cliente = c.id
JOIN produtos p ON v.id_produto = p.id_produto
GROUP BY c.id, c.nome, c.cidade
ORDER BY receita_total DESC;
