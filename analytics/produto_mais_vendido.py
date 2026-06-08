"""
Analytics script: Find most sold product using DuckDB on Parquet files.
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
    PROCESSED_PRODUCTS_FILE,
    ANALYTICS_TOP_PRODUCT_FILE,
    TOP_PRODUCT_SQL
)


def find_top_product():
    """
    Find the most sold product from sales data using DuckDB.
    Results are saved to a Parquet file.
    """
    print("Finding most sold product...")
    
    # Read SQL query from file
    with open(TOP_PRODUCT_SQL, 'r') as f:
        sql_query = f.read()
    
    # Adapt query for DuckDB with Parquet files
    duckdb_query = sql_query.replace('FROM vendas v', f"FROM read_parquet('{PROCESSED_SALES_FILE}') v")
    duckdb_query = duckdb_query.replace('JOIN produtos p', f"JOIN read_parquet('{PROCESSED_PRODUCTS_FILE}') p")
    
    # Execute query with DuckDB
    df = duckdb.sql(duckdb_query).df()
    
    print("Most Sold Product Results:")
    print(df.to_string(index=False))
    
    # Save to Parquet
    df.to_parquet(ANALYTICS_TOP_PRODUCT_FILE, index=False)
    print(f"\nResults saved to {ANALYTICS_TOP_PRODUCT_FILE}")
    
    return df


if __name__ == "__main__":
    find_top_product()