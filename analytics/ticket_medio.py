"""
Analytics script: Calculate average ticket using DuckDB on Curated Layer.
This script reads from the Curated Layer (data/curated/) and saves results to analytics layer.
"""

import sys
from pathlib import Path

import duckdb
import pandas as pd

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent))

from config.settings import DATA_DIR, ANALYTICS_DATA_DIR


def calculate_average_ticket():
    """
    Calculate average ticket from Curated Layer using DuckDB.
    Results are saved to a Parquet file in the analytics layer.
    """
    print("Calculating average ticket from Curated Layer...")
    
    # Read SQL query from file
    sql_file = Path(__file__).parent.parent / "sql" / "analytics" / "ticket_medio.sql"
    with open(sql_file, 'r') as f:
        sql_query = f.read()
    
    # Adapt query to use absolute paths
    curated_dir = DATA_DIR / "curated"
    fato_vendas_path = curated_dir / "fato_vendas.parquet"
    
    duckdb_query = sql_query.replace(
        "read_parquet('data/curated/fato_vendas.parquet')",
        f"read_parquet('{fato_vendas_path}')"
    )
    
    # Execute query with DuckDB
    df = duckdb.sql(duckdb_query).df()
    
    print("Average Ticket Results:")
    print(df.to_string(index=False))
    
    # Save to analytics layer
    output_file = ANALYTICS_DATA_DIR / "ticket_medio.parquet"
    df.to_parquet(output_file, index=False)
    print(f"\nResults saved to {output_file}")
    
    return df


if __name__ == "__main__":
    calculate_average_ticket()
