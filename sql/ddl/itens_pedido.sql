-- DDL script to create itens_pedido table in ERP (PostgreSQL)
-- This represents the operational system source table for order items

CREATE TABLE IF NOT EXISTS itens_pedido (
    id_item SERIAL PRIMARY KEY,
    id_pedido INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    preco_unitario DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) GENERATED ALWAYS AS (quantidade * preco_unitario) STORED,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido),
    FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_itens_pedido_id_pedido ON itens_pedido(id_pedido);
CREATE INDEX IF NOT EXISTS idx_itens_pedido_id_produto ON itens_pedido(id_produto);
