"""
Transform script: Extract data from PostgreSQL, transform with Pandas, and export to Parquet.
This script reads data from PostgreSQL tables and saves them as Parquet files.
"""

import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent.parent))

from config.settings import (
    DATABASE_URL,
    PROCESSED_CLIENTS_FILE,
    PROCESSED_PRODUCTS_FILE,
    PROCESSED_SALES_FILE
)


def extract_table_to_parquet(table_name: str, output_file: Path):
    """
    Extract data from a PostgreSQL table and save as Parquet.
    
    Args:
        table_name: Name of the table to extract
        output_file: Path to save the Parquet file
    """
    print(f"Extracting data from table: {table_name}")
    
    # Create SQLAlchemy engine
    engine = create_engine(DATABASE_URL)
    
    # Read data from PostgreSQL
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)
    
    print(f"Loaded {len(df)} records from {table_name}")
    
    # Save to Parquet
    df.to_parquet(output_file, index=False)
    print(f"Saved to {output_file}")
    
    return df


def transform_and_export():
    """
    Main transformation function: Extract all tables and export to Parquet.
    """
    print("Starting transformation process...")
    
    # Extract and export each table
    df_clientes = extract_table_to_parquet('clientes', PROCESSED_CLIENTS_FILE)
    df_produtos = extract_table_to_parquet('produtos', PROCESSED_PRODUCTS_FILE)
    df_vendas = extract_table_to_parquet('vendas', PROCESSED_SALES_FILE)
    
    print("\nTransformation completed successfully!")
    print(f"Clientes: {len(df_clientes)} records")
    print(f"Produtos: {len(df_produtos)} records")
    print(f"Vendas: {len(df_vendas)} records")
    
    return df_clientes, df_produtos, df_vendas


if __name__ == "__main__":
    transform_and_export()
