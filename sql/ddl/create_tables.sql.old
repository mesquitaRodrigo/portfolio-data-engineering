-- DDL script to create tables for the portfolio data engineering project
-- This script is automatically executed when PostgreSQL container starts

-- Create clientes table
CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL
);

-- Create produtos table
CREATE TABLE IF NOT EXISTS produtos (
    id_produto SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL
);

-- Create vendas table
CREATE TABLE IF NOT EXISTS vendas (
    id_venda SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    data_venda DATE NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id),
    FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_vendas_id_cliente ON vendas(id_cliente);
CREATE INDEX IF NOT EXISTS idx_vendas_id_produto ON vendas(id_produto);
CREATE INDEX IF NOT EXISTS idx_vendas_data_venda ON vendas(data_venda);
