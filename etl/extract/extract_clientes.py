"""
Extract script: Extract clientes table from ERP (PostgreSQL) to Raw Layer.
This script reads from the operational system and saves to Parquet in data/raw/.
"""

import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent.parent))

from config.settings import DATABASE_URL, RAW_DATA_DIR


def extract_clientes():
    """
    Extract clientes data from PostgreSQL and save to Parquet in Raw Layer.
    """
    print("Starting clientes extraction process...")
    
    # Create SQLAlchemy engine
    engine = create_engine(DATABASE_URL)
    
    # Read SQL query from file
    sql_file = Path(__file__).parent.parent.parent / "sql" / "extract" / "clientes.sql"
    with open(sql_file, 'r') as f:
        query = f.read()
    
    # Extract data from PostgreSQL
    print(f"Extracting clientes data from PostgreSQL...")
    df_clientes = pd.read_sql(query, engine)
    print(f"Extracted {len(df_clientes)} clientes records")
    
    # Save to Raw Layer as Parquet
    output_file = RAW_DATA_DIR / "clientes.parquet"
    df_clientes.to_parquet(output_file, index=False)
    print(f"Saved to {output_file}")
    
    print("Clientes extraction completed successfully!")


if __name__ == "__main__":
    extract_clientes()
