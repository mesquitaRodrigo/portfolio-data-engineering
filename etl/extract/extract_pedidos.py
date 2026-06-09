"""
Extract script: Extract pedidos table from ERP (PostgreSQL) to Raw Layer.
This script reads from the operational system and saves to Parquet in data/raw/.
"""

import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent.parent))

from config.settings import DATABASE_URL, RAW_DATA_DIR


def extract_pedidos():
    """
    Extract pedidos data from PostgreSQL and save to Parquet in Raw Layer.
    """
    print("Starting pedidos extraction process...")
    
    # Create SQLAlchemy engine
    engine = create_engine(DATABASE_URL)
    
    # Read SQL query from file
    sql_file = Path(__file__).parent.parent.parent / "sql" / "extract" / "pedidos.sql"
    with open(sql_file, 'r') as f:
        query = f.read()
    
    # Extract data from PostgreSQL
    print(f"Extracting pedidos data from PostgreSQL...")
    df_pedidos = pd.read_sql(query, engine)
    print(f"Extracted {len(df_pedidos)} pedidos records")
    
    # Save to Raw Layer as Parquet
    output_file = RAW_DATA_DIR / "pedidos.parquet"
    df_pedidos.to_parquet(output_file, index=False)
    print(f"Saved to {output_file}")
    
    print("Pedidos extraction completed successfully!")


if __name__ == "__main__":
    extract_pedidos()
