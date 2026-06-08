"""
Load script: Load data from Parquet files into PostgreSQL.
This script reads Parquet files and loads them into PostgreSQL tables.
"""

import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent.parent))

from config.settings import DATABASE_URL


def load_parquet_to_postgres(parquet_file: Path, table_name: str, if_exists: str = 'replace'):
    """
    Load data from a Parquet file into a PostgreSQL table.
    
    Args:
        parquet_file: Path to the Parquet file
        table_name: Name of the target table in PostgreSQL
        if_exists: How to behave if the table exists ('fail', 'replace', 'append')
    """
    print(f"Loading data from {parquet_file} to table {table_name}")
    
    # Read Parquet file
    df = pd.read_parquet(parquet_file)
    print(f"Loaded {len(df)} records from Parquet file")
    
    # Create SQLAlchemy engine
    engine = create_engine(DATABASE_URL)
    
    # Load to PostgreSQL
    df.to_sql(table_name, engine, if_exists=if_exists, index=False)
    print(f"Successfully loaded data to {table_name}")


def load_analytics_results():
    """
    Load analytics results from Parquet files to PostgreSQL.
    This creates tables for analytics results in the database.
    """
    print("Starting load process for analytics results...")
    
    # Load revenue by client
    load_parquet_to_postgres(
        Path(__file__).parent.parent.parent / 'data' / 'analytics' / 'receita_por_cliente.parquet',
        'analytics_receita_por_cliente',
        if_exists='replace'
    )
    
    # Load top product
    load_parquet_to_postgres(
        Path(__file__).parent.parent.parent / 'data' / 'analytics' / 'produto_mais_vendido.parquet',
        'analytics_produto_mais_vendido',
        if_exists='replace'
    )
    
    # Load total revenue
    load_parquet_to_postgres(
        Path(__file__).parent.parent.parent / 'data' / 'analytics' / 'receita_total.parquet',
        'analytics_receita_total',
        if_exists='replace'
    )
    
    print("Analytics results loaded successfully!")


if __name__ == "__main__":
    load_analytics_results()
