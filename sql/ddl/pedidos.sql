-- DDL script to create pedidos table in ERP (PostgreSQL)
-- This represents the operational system source table for orders

CREATE TABLE IF NOT EXISTS pedidos (
    id_pedido SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL,
    data_pedido DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'pendente',
    valor_total DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_pedidos_id_cliente ON pedidos(id_cliente);
CREATE INDEX IF NOT EXISTS idx_pedidos_data_pedido ON pedidos(data_pedido);
CREATE INDEX IF NOT EXISTS idx_pedidos_status ON pedidos(status);
