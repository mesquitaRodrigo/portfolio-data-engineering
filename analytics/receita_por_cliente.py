"""
Analytics script: Calculate revenue by client using DuckDB on Parquet files.
This script loads the SQL query from a file and executes it with DuckDB.
"""

import sys
from pathlib import Path

import duckdb
import pandas as pd

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent))

from config.settings import (
    PROCESSED_SALES_FILE,
    PROCESSED_CLIENTS_FILE,
    PROCESSED_PRODUCTS_FILE,
    ANALYTICS_REVENUE_BY_CLIENT_FILE,
    REVENUE_BY_CLIENT_SQL
)


def calculate_revenue_by_client():
    """
    Calculate revenue by client from sales data using DuckDB.
    Results are saved to a Parquet file.
    """
    print("Calculating revenue by client...")
    
    # Read SQL query from file
    with open(REVENUE_BY_CLIENT_SQL, 'r') as f:
        sql_query = f.read()
    
    # Adapt query for DuckDB with Parquet files
    duckdb_query = sql_query.replace('FROM vendas v', f"FROM read_parquet('{PROCESSED_SALES_FILE}') v")
    duckdb_query = duckdb_query.replace('JOIN clientes c', f"JOIN read_parquet('{PROCESSED_CLIENTS_FILE}') c")
    duckdb_query = duckdb_query.replace('JOIN produtos p', f"JOIN read_parquet('{PROCESSED_PRODUCTS_FILE}') p")
    
    # Execute query with DuckDB
    df = duckdb.sql(duckdb_query).df()
    
    print("Revenue by Client Results:")
    print(df.to_string(index=False))
    
    # Save to Parquet
    df.to_parquet(ANALYTICS_REVENUE_BY_CLIENT_FILE, index=False)
    print(f"\nResults saved to {ANALYTICS_REVENUE_BY_CLIENT_FILE}")
    
    return df


if __name__ == "__main__":
    calculate_revenue_by_client()