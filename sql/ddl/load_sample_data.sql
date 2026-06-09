-- Sample Data Load Script - ERP Schema
-- Sprint 1: Evolução do ERP Operacional
-- Dados de exemplo para teste e desenvolvimento

-- Insert clientes (10 clientes)
INSERT INTO clientes (nome, cidade) VALUES
('João Silva', 'São Paulo'),
('Maria Santos', 'Rio de Janeiro'),
('Carlos Oliveira', 'Belo Horizonte'),
('Ana Costa', 'Brasília'),
('Pedro Ferreira', 'Salvador'),
('Lucia Mendes', 'Curitiba'),
('Ricardo Alves', 'Fortaleza'),
('Fernanda Lima', 'Manaus'),
('Roberto Carvalho', 'Porto Alegre'),
('Juliana Martins', 'Recife');

-- Insert produtos (10 produtos)
INSERT INTO produtos (nome, categoria, preco) VALUES
('Notebook Dell Inspiron', 'Eletrônicos', 3500.00),
('Smartphone Samsung Galaxy', 'Eletrônicos', 2500.00),
('Monitor LG 24"', 'Eletrônicos', 800.00),
('Teclado Mecânico', 'Acessórios', 250.00),
('Mouse Wireless', 'Acessórios', 120.00),
('Cadeira Gamer', 'Móveis', 1200.00),
('Mesa Escritório', 'Móveis', 800.00),
('Headset Logitech', 'Acessórios', 350.00),
('Webcam HD', 'Eletrônicos', 400.00),
('SSD 1TB', 'Eletrônicos', 450.00);

-- Insert pedidos (20 pedidos distribuídos entre clientes)
INSERT INTO pedidos (id_cliente, data_pedido) VALUES
(1, '2024-01-15'),  -- João Silva
(2, '2024-01-16'),  -- Maria Santos
(3, '2024-01-17'),  -- Carlos Oliveira
(1, '2024-01-18'),  -- João Silva (segundo pedido)
(4, '2024-01-19'),  -- Ana Costa
(5, '2024-01-20'),  -- Pedro Ferreira
(2, '2024-01-21'),  -- Maria Santos (segundo pedido)
(6, '2024-01-22'),  -- Lucia Mendes
(7, '2024-01-23'),  -- Ricardo Alves
(3, '2024-01-24'),  -- Carlos Oliveira (segundo pedido)
(8, '2024-01-25'),  -- Fernanda Lima
(9, '2024-01-26'),  -- Roberto Carvalho
(4, '2024-01-27'),  -- Ana Costa (segundo pedido)
(10, '2024-01-28'), -- Juliana Martins
(5, '2024-01-29'),  -- Pedro Ferreira (segundo pedido)
(6, '2024-02-01'),  -- Lucia Mendes (segundo pedido)
(7, '2024-02-02'),  -- Ricardo Alves (segundo pedido)
(8, '2024-02-03'),  -- Fernanda Lima (segundo pedido)
(9, '2024-02-04'),  -- Roberto Carvalho (segundo pedido)
(10, '2024-02-05'); -- Juliana Martins (segundo pedido)

-- Insert itens_pedido (50 itens distribuídos entre pedidos)
-- Pedido 1: João Silva - Notebook + Monitor
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(1, 1, 1, 3500.00),
(1, 3, 1, 800.00);

-- Pedido 2: Maria Santos - Smartphone + Teclado
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(2, 2, 1, 2500.00),
(2, 4, 1, 250.00);

-- Pedido 3: Carlos Oliveira - Cadeira + Mesa
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(3, 6, 1, 1200.00),
(3, 7, 1, 800.00);

-- Pedido 4: João Silva - Mouse + Headset
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(4, 5, 2, 120.00),
(4, 8, 1, 350.00);

-- Pedido 5: Ana Costa - Notebook + SSD
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(5, 1, 1, 3500.00),
(5, 10, 2, 450.00);

-- Pedido 6: Pedro Ferreira - Monitor + Teclado + Mouse
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(6, 3, 2, 800.00),
(6, 4, 1, 250.00),
(6, 5, 1, 120.00);

-- Pedido 7: Maria Santos - Webcam
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(7, 9, 1, 400.00);

-- Pedido 8: Lucia Mendes - Smartphone + Monitor
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(8, 2, 1, 2500.00),
(8, 3, 1, 800.00);

-- Pedido 9: Ricardo Alves - Cadeira + Teclado + Mouse
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(9, 6, 1, 1200.00),
(9, 4, 1, 250.00),
(9, 5, 1, 120.00);

-- Pedido 10: Carlos Oliveira - SSD + Headset
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(10, 10, 2, 450.00),
(10, 8, 1, 350.00);

-- Pedido 11: Fernanda Lima - Notebook + Monitor + Teclado
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(11, 1, 1, 3500.00),
(11, 3, 1, 800.00),
(11, 4, 1, 250.00);

-- Pedido 12: Roberto Carvalho - Smartphone + SSD
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(12, 2, 1, 2500.00),
(12, 10, 1, 450.00);

-- Pedido 13: Ana Costa - Cadeira + Headset
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(13, 6, 1, 1200.00),
(13, 8, 1, 350.00);

-- Pedido 14: Juliana Martins - Monitor + Webcam
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(14, 3, 1, 800.00),
(14, 9, 1, 400.00);

-- Pedido 15: Pedro Ferreira - Notebook + Teclado + Mouse
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(15, 1, 1, 3500.00),
(15, 4, 1, 250.00),
(15, 5, 1, 120.00);

-- Pedido 16: Lucia Mendes - SSD + Monitor
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(16, 10, 2, 450.00),
(16, 3, 1, 800.00);

-- Pedido 17: Ricardo Alves - Smartphone + Headset + Webcam
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(17, 2, 1, 2500.00),
(17, 8, 1, 350.00),
(17, 9, 1, 400.00);

-- Pedido 18: Fernanda Lima - Cadeira + Mesa
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(18, 6, 1, 1200.00),
(18, 7, 1, 800.00);

-- Pedido 19: Roberto Carvalho - Teclado + Mouse + SSD
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(19, 4, 1, 250.00),
(19, 5, 1, 120.00),
(19, 10, 1, 450.00);

-- Pedido 20: Juliana Martins - Notebook + Monitor + Headset
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(20, 1, 1, 3500.00),
(20, 3, 1, 800.00),
(20, 8, 1, 350.00);

-- Verify data counts
SELECT 'clientes' as tabela, COUNT(*) as quantidade FROM clientes
UNION ALL
SELECT 'produtos', COUNT(*) FROM produtos
UNION ALL
SELECT 'pedidos', COUNT(*) FROM pedidos
UNION ALL
SELECT 'itens_pedido', COUNT(*) FROM itens_pedido;
