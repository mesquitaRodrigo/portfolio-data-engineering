-- DDL script to create clientes table in ERP (PostgreSQL)
-- This represents the operational system source table

CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefone VARCHAR(20),
    data_cadastro DATE DEFAULT CURRENT_DATE,
    ativo BOOLEAN DEFAULT TRUE
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_clientes_cidade ON clientes(cidade);
CREATE INDEX IF NOT EXISTS idx_clientes_ativo ON clientes(ativo);
