SELECT
    p.id_pedido,
    p.data_pedido,
    c.id_cliente,
    c.nome AS cliente,
    c.cidade,
    pr.id_produto,
    pr.nome AS produto,
    pr.categoria,
    ip.quantidade,
    ip.preco_unitario,
    (ip.quantidade * ip.preco_unitario) AS valor_total
FROM pedidos p
JOIN clientes c
    ON p.id_cliente = c.id_cliente
JOIN itens_pedido ip
    ON p.id_pedido = ip.id_pedido
JOIN produtos pr
    ON ip.id_produto = pr.id_produto;