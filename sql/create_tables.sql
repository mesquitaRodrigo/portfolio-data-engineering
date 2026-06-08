-- Create vendas table
CREATE TABLE vendas (
    id_venda SERIAL PRIMARY KEY,
    id_cliente INTEGER,
    id_produto INTEGER,
    quantidade INTEGER,
    data_venda DATE,

    FOREIGN KEY (id_cliente)
        REFERENCES clientes(id),

    FOREIGN KEY (id_produto)
        REFERENCES produtos(id_produto)
);

-- Insert sample data into vendas
INSERT INTO vendas (id_cliente, id_produto, quantidade, data_venda)
VALUES
    (1, 1, 1, '2025-01-01'),
    (2, 2, 2, '2025-01-01'),
    (3, 3, 1, '2025-01-01'),
    (3, 4, 3, '2025-01-02'),
    (1, 2, 1, '2025-01-02'),
    (2, 3, 2, '2025-01-03'),
    (3, 4, 1, '2025-01-04'),
    (2, 1, 3, '2025-01-04');
