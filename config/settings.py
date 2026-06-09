"""
Centralized configuration settings for the Data Engineering Portfolio Project.
All database credentials and paths are defined here for easy management.
Architecture: ERP (PostgreSQL) → Raw Layer → Curated Layer → DuckDB → Analytics
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Database Configuration (ERP - PostgreSQL)
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5434")),
    "database": os.getenv("DB_NAME", "portfolio_db"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "admin123"),
}

# SQLAlchemy Database URL
DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# Directory Paths - Data Lake Architecture
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"           # Raw Layer - Extracted from ERP
CURATED_DATA_DIR = DATA_DIR / "curated"   # Curated Layer - Dimensional Model
ANALYTICS_DATA_DIR = DATA_DIR / "analytics"  # Analytics Layer - Business Metrics

# SQL Directory Paths
SQL_DIR = BASE_DIR / "sql"
DDL_DIR = SQL_DIR / "ddl"                # Database Schema Definitions
EXTRACT_SQL_DIR = SQL_DIR / "extract"    # Extract Queries (ERP → Raw)
TRANSFORM_SQL_DIR = SQL_DIR / "transform"  # Transform Queries (Raw → Curated)
ANALYTICS_SQL_DIR = SQL_DIR / "analytics"  # Analytics Queries (Curated → Analytics)

# ETL Directory Paths
ETL_DIR = BASE_DIR / "etl"
EXTRACT_DIR = ETL_DIR / "extract"        # Extract Scripts
TRANSFORM_DIR = ETL_DIR / "transform"    # Transform Scripts
LOAD_DIR = ETL_DIR / "load"              # Load Scripts

# Analytics Directory Paths
ANALYTICS_DIR = BASE_DIR / "analytics"   # Analytics Python Scripts

# Docs Directory Paths
DOCS_DIR = BASE_DIR / "docs"             # Documentation

# Raw Layer File Paths (Extracted from ERP)
RAW_CLIENTES_FILE = RAW_DATA_DIR / "clientes.parquet"
RAW_PRODUTOS_FILE = RAW_DATA_DIR / "produtos.parquet"
RAW_PEDIDOS_FILE = RAW_DATA_DIR / "pedidos.parquet"
RAW_ITENS_PEDIDO_FILE = RAW_DATA_DIR / "itens_pedido.parquet"

# Curated Layer File Paths (Dimensional Model)
CURATED_DIM_CLIENTE_FILE = CURATED_DATA_DIR / "dim_cliente.parquet"
CURATED_DIM_PRODUTO_FILE = CURATED_DATA_DIR / "dim_produto.parquet"
CURATED_DIM_DATA_FILE = CURATED_DATA_DIR / "dim_data.parquet"
CURATED_FATO_VENDAS_FILE = CURATED_DATA_DIR / "fato_vendas.parquet"

# Analytics Layer File Paths (Business Metrics)
ANALYTICS_RECEITA_TOTAL_FILE = ANALYTICS_DATA_DIR / "receita_total.parquet"
ANALYTICS_RECEITA_POR_CLIENTE_FILE = ANALYTICS_DATA_DIR / "receita_por_cliente.parquet"
ANALYTICS_RECEITA_POR_PRODUTO_FILE = ANALYTICS_DATA_DIR / "receita_por_produto.parquet"
ANALYTICS_RECEITA_POR_CIDADE_FILE = ANALYTICS_DATA_DIR / "receita_por_cidade.parquet"
ANALYTICS_TICKET_MEDIO_FILE = ANALYTICS_DATA_DIR / "ticket_medio.parquet"
ANALYTICS_PRODUTO_MAIS_VENDIDO_FILE = ANALYTICS_DATA_DIR / "produto_mais_vendido.parquet"

# SQL File Paths - DDL (ERP Schema)
DDL_CLIENTES_SQL = DDL_DIR / "clientes.sql"
DDL_PRODUTOS_SQL = DDL_DIR / "produtos.sql"
DDL_PEDIDOS_SQL = DDL_DIR / "pedidos.sql"
DDL_ITENS_PEDIDO_SQL = DDL_DIR / "itens_pedido.sql"

# SQL File Paths - Extract (ERP → Raw)
EXTRACT_CLIENTES_SQL = EXTRACT_SQL_DIR / "clientes.sql"
EXTRACT_PRODUTOS_SQL = EXTRACT_SQL_DIR / "produtos.sql"
EXTRACT_PEDIDOS_SQL = EXTRACT_SQL_DIR / "pedidos.sql"
EXTRACT_ITENS_PEDIDO_SQL = EXTRACT_SQL_DIR / "itens_pedido.sql"

# SQL File Paths - Transform (Raw → Curated)
TRANSFORM_DIM_CLIENTE_SQL = TRANSFORM_SQL_DIR / "dim_cliente.sql"
TRANSFORM_DIM_PRODUTO_SQL = TRANSFORM_SQL_DIR / "dim_produto.sql"
TRANSFORM_FATO_VENDAS_SQL = TRANSFORM_SQL_DIR / "fato_vendas.sql"

# SQL File Paths - Analytics (Curated → Analytics)
ANALYTICS_RECEITA_TOTAL_SQL = ANALYTICS_SQL_DIR / "receita_total.sql"
ANALYTICS_RECEITA_POR_CLIENTE_SQL = ANALYTICS_SQL_DIR / "receita_por_cliente.sql"
ANALYTICS_RECEITA_POR_PRODUTO_SQL = ANALYTICS_SQL_DIR / "receita_por_produto.sql"
ANALYTICS_RECEITA_POR_CIDADE_SQL = ANALYTICS_SQL_DIR / "receita_por_cidade.sql"
ANALYTICS_TICKET_MEDIO_SQL = ANALYTICS_SQL_DIR / "ticket_medio.sql"
ANALYTICS_PRODUTO_MAIS_VENDIDO_SQL = ANALYTICS_SQL_DIR / "produto_mais_vendido.sql"

# Create directories if they don't exist
for directory in [
    RAW_DATA_DIR, 
    CURATED_DATA_DIR, 
    ANALYTICS_DATA_DIR, 
    DDL_DIR, 
    EXTRACT_SQL_DIR, 
    TRANSFORM_SQL_DIR, 
    ANALYTICS_SQL_DIR,
    DOCS_DIR
]:
    directory.mkdir(parents=True, exist_ok=True)
