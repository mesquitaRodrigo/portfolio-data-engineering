-- ERP Schema DDL - Portfolio Data Engineering
-- Sistema Operacional (OLTP) - Modelo Relacional
-- Sprint 1: Evolução do ERP Operacional

-- Drop existing tables if they exist (in correct order due to FK dependencies)
DROP TABLE IF EXISTS itens_pedido CASCADE;
DROP TABLE IF EXISTS pedidos CASCADE;
DROP TABLE IF EXISTS produtos CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;

-- Create clientes table
CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    CONSTRAINT chk_nome_not_empty CHECK (LENGTH(TRIM(nome)) > 0),
    CONSTRAINT chk_cidade_not_empty CHECK (LENGTH(TRIM(cidade)) > 0)
);

-- Create produtos table
CREATE TABLE produtos (
    id_produto SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL CHECK (preco > 0),
    CONSTRAINT chk_produto_nome_not_empty CHECK (LENGTH(TRIM(nome)) > 0),
    CONSTRAINT chk_categoria_not_empty CHECK (LENGTH(TRIM(categoria)) > 0)
);

-- Create pedidos table
CREATE TABLE pedidos (
    id_pedido SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL,
    data_pedido DATE NOT NULL DEFAULT CURRENT_DATE,
    CONSTRAINT fk_pedidos_clientes 
        FOREIGN KEY (id_cliente) 
        REFERENCES clientes(id_cliente)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT chk_data_pedido_valid CHECK (data_pedido <= CURRENT_DATE)
);

-- Create itens_pedido table
CREATE TABLE itens_pedido (
    id_item SERIAL PRIMARY KEY,
    id_pedido INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario DECIMAL(10, 2) NOT NULL CHECK (preco_unitario > 0),
    CONSTRAINT fk_itens_pedido_pedidos 
        FOREIGN KEY (id_pedido) 
        REFERENCES pedidos(id_pedido)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_itens_pedido_produtos 
        FOREIGN KEY (id_produto) 
        REFERENCES produtos(id_produto)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Create indexes for better query performance
-- Indexes on foreign keys for join performance
CREATE INDEX idx_pedidos_id_cliente ON pedidos(id_cliente);
CREATE INDEX idx_pedidos_data_pedido ON pedidos(data_pedido);
CREATE INDEX idx_itens_pedido_id_pedido ON itens_pedido(id_pedido);
CREATE INDEX idx_itens_pedido_id_produto ON itens_pedido(id_produto);

-- Composite index for common analytical queries
CREATE INDEX idx_itens_pedido_pedido_produto ON itens_pedido(id_pedido, id_produto);

-- Index on cidade for customer analytics
CREATE INDEX idx_clientes_cidade ON clientes(cidade);

-- Index on categoria for product analytics
CREATE INDEX idx_produtos_categoria ON produtos(categoria);

-- Add comments for documentation
COMMENT ON TABLE clientes IS 'Tabela de clientes do ERP - Sistema Operacional';
COMMENT ON TABLE produtos IS 'Tabela de produtos do ERP - Sistema Operacional';
COMMENT ON TABLE pedidos IS 'Tabela de pedidos do ERP - Sistema Operacional';
COMMENT ON TABLE itens_pedido IS 'Tabela de itens de pedido do ERP - Sistema Operacional';

COMMENT ON COLUMN clientes.id_cliente IS 'Identificador único do cliente (PK)';
COMMENT ON COLUMN clientes.nome IS 'Nome completo do cliente';
COMMENT ON COLUMN clientes.cidade IS 'Cidade do cliente';

COMMENT ON COLUMN produtos.id_produto IS 'Identificador único do produto (PK)';
COMMENT ON COLUMN produtos.nome IS 'Nome do produto';
COMMENT ON COLUMN produtos.categoria IS 'Categoria do produto';
COMMENT ON COLUMN produtos.preco IS 'Preço unitário do produto';

COMMENT ON COLUMN pedidos.id_pedido IS 'Identificador único do pedido (PK)';
COMMENT ON COLUMN pedidos.id_cliente IS 'Identificador do cliente (FK)';
COMMENT ON COLUMN pedidos.data_pedido IS 'Data do pedido';

COMMENT ON COLUMN itens_pedido.id_item IS 'Identificador único do item (PK)';
COMMENT ON COLUMN itens_pedido.id_pedido IS 'Identificador do pedido (FK)';
COMMENT ON COLUMN itens_pedido.id_produto IS 'Identificador do produto (FK)';
COMMENT ON COLUMN itens_pedido.quantidade IS 'Quantidade de itens no pedido';
COMMENT ON COLUMN itens_pedido.preco_unitario IS 'Preço unitário na data da venda';
