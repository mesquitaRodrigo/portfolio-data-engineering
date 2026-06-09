-- Transform script to create fato_vendas from Raw Layer
-- This query transforms raw order and item data into a fact table
-- Used to populate the Curated Layer (data/curated/fato_vendas.parquet)

-- Note: This SQL is designed to work with DuckDB on Parquet files
-- Replace 'data/raw/' with actual path to raw layer

SELECT 
    ip.id_item as sk_venda,
    ip.id_pedido as nk_pedido,
    ip.id_produto as sk_produto,
    p.id_cliente as sk_cliente,
    ip.quantidade,
    ip.preco_unitario,
    ip.subtotal as valor_total,
    p.data_pedido as data_venda,
    p.status,
    ip.extract_timestamp,
    CURRENT_TIMESTAMP as dw_load_timestamp
FROM read_parquet('data/raw/itens_pedido.parquet') ip
INNER JOIN read_parquet('data/raw/pedidos.parquet') p ON ip.id_pedido = p.id_pedido
WHERE p.status IN ('concluido', 'enviado', 'entregue');
