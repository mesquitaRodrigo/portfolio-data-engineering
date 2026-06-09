-- Extract script for itens_pedido table from ERP (PostgreSQL)
-- This query extracts all order item data without transformation
-- Used to populate the Raw Layer (data/raw/itens_pedido.parquet)

SELECT 
    ip.id_item,
    ip.id_pedido,
    ip.id_produto,
    ip.quantidade,
    ip.preco_unitario,
    ip.subtotal,
    p.data_pedido,
    NOW() as extract_timestamp
FROM itens_pedido ip
INNER JOIN pedidos p ON ip.id_pedido = p.id_pedido
WHERE p.status IN ('concluido', 'enviado', 'entregue');
