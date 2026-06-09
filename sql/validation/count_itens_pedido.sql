-- Validation Query: Count itens_pedido
-- Verifica a quantidade de registros na tabela itens_pedido

SELECT 
    'itens_pedido' as tabela,
    COUNT(*) as total_registros,
    MIN(id_item) as menor_id,
    MAX(id_item) as maior_id,
    COUNT(DISTINCT id_pedido) as pedidos_unicos,
    COUNT(DISTINCT id_produto) as produtos_unicos,
    SUM(quantidade) as quantidade_total_itens
FROM itens_pedido;
