-- Validation Query: Count pedidos
-- Verifica a quantidade de registros na tabela pedidos

SELECT 
    'pedidos' as tabela,
    COUNT(*) as total_registros,
    MIN(id_pedido) as menor_id,
    MAX(id_pedido) as maior_id,
    MIN(data_pedido) as data_mais_antiga,
    MAX(data_pedido) as data_mais_recente,
    COUNT(DISTINCT id_cliente) as clientes_unicos
FROM pedidos;
