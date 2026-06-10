-- Data Warehouse Schema Creation Script
-- Creates the dw schema and all dimensional tables for the data warehouse
-- Sprint 6 - Materialização do Data Warehouse no PostgreSQL

-- Create dw schema
CREATE SCHEMA IF NOT EXISTS dw;

-- Drop existing tables if they exist (for clean re-creation)
DROP TABLE IF EXISTS dw.fato_vendas CASCADE;
DROP TABLE IF EXISTS dw.dim_data CASCADE;
DROP TABLE IF EXISTS dw.dim_produto CASCADE;
DROP TABLE IF EXISTS dw.dim_cliente CASCADE;

-- Create dim_cliente table
CREATE TABLE dw.dim_cliente (
    id_cliente INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL
);

-- Create dim_produto table
CREATE TABLE dw.dim_produto (
    id_produto INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    preco NUMERIC(10, 2) NOT NULL
);

-- Create dim_data table
CREATE TABLE dw.dim_data (
    data DATE PRIMARY KEY,
    ano INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    dia INTEGER NOT NULL,
    trimestre INTEGER NOT NULL,
    nome_mes VARCHAR(20) NOT NULL
);

-- Create fato_vendas table
CREATE TABLE dw.fato_vendas (
    id_pedido INTEGER NOT NULL,
    data_pedido DATE NOT NULL,
    id_cliente INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    preco_unitario NUMERIC(10, 2) NOT NULL,
    valor_total NUMERIC(10, 2) NOT NULL,
    PRIMARY KEY (id_pedido, id_produto),
    FOREIGN KEY (id_cliente) REFERENCES dw.dim_cliente(id_cliente),
    FOREIGN KEY (id_produto) REFERENCES dw.dim_produto(id_produto),
    FOREIGN KEY (data_pedido) REFERENCES dw.dim_data(data)
);

-- Create indexes for performance
CREATE INDEX idx_fato_vendas_data_pedido ON dw.fato_vendas(data_pedido);
CREATE INDEX idx_fato_vendas_id_cliente ON dw.fato_vendas(id_cliente);
CREATE INDEX idx_fato_vendas_id_produto ON dw.fato_vendas(id_produto);
CREATE INDEX idx_dim_data_ano ON dw.dim_data(ano);
CREATE INDEX idx_dim_data_mes ON dw.dim_data(mes);
CREATE INDEX idx_dim_data_trimestre ON dw.dim_data(trimestre);

-- Grant permissions (optional - adjust as needed)
-- GRANT SELECT ON ALL TABLES IN SCHEMA dw TO admin;
-- GRANT USAGE ON SCHEMA dw TO admin;
