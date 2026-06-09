-- Extract script for pedidos table from ERP (PostgreSQL)
-- This query extracts all order data without transformation
-- Used to populate the Raw Layer (data/raw/pedidos.parquet)

SELECT 
    id_pedido,
    id_cliente,
    data_pedido,
    status,
    valor_total,
    NOW() as extract_timestamp
FROM pedidos
WHERE status IN ('concluido', 'enviado', 'entregue');
