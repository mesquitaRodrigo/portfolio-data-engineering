"""
Centralized configuration settings for the Data Engineering Portfolio Project.
All database credentials and paths are defined here for easy management.
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Database Configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "portfolio_db"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "admin123"),
}

# SQLAlchemy Database URL
DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

# Directory Paths
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
ANALYTICS_DATA_DIR = DATA_DIR / "analytics"

SQL_DIR = BASE_DIR / "sql"
DDL_DIR = SQL_DIR / "ddl"
ANALYTICS_SQL_DIR = SQL_DIR / "analytics"

ETL_DIR = BASE_DIR / "etl"
ANALYTICS_DIR = BASE_DIR / "analytics"

# File Paths
RAW_SALES_FILE = RAW_DATA_DIR / "vendas.csv"
PROCESSED_CLIENTS_FILE = PROCESSED_DATA_DIR / "clientes.parquet"
PROCESSED_PRODUCTS_FILE = PROCESSED_DATA_DIR / "produtos.parquet"
PROCESSED_SALES_FILE = PROCESSED_DATA_DIR / "vendas.parquet"

ANALYTICS_REVENUE_BY_CLIENT_FILE = ANALYTICS_DATA_DIR / "receita_por_cliente.parquet"
ANALYTICS_TOP_PRODUCT_FILE = ANALYTICS_DATA_DIR / "produto_mais_vendido.parquet"
ANALYTICS_REVENUE_TOTAL_FILE = ANALYTICS_DATA_DIR / "receita_total.parquet"

# SQL File Paths
CREATE_TABLES_SQL = DDL_DIR / "create_tables.sql"
REVENUE_TOTAL_SQL = ANALYTICS_SQL_DIR / "receita_total.sql"
REVENUE_BY_CLIENT_SQL = ANALYTICS_SQL_DIR / "receita_por_cliente.sql"
TOP_PRODUCT_SQL = ANALYTICS_SQL_DIR / "produto_mais_vendido.sql"

# Create directories if they don't exist
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, ANALYTICS_DATA_DIR, DDL_DIR, ANALYTICS_SQL_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
