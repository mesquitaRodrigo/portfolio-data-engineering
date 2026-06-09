"""
Extract script: Extract produtos table from ERP (PostgreSQL) to Raw Layer.
This script reads from the operational system and saves to Parquet in data/raw/.
"""

import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent.parent))

from config.settings import DATABASE_URL, RAW_DATA_DIR


def extract_produtos():
    """
    Extract produtos data from PostgreSQL and save to Parquet in Raw Layer.
    """
    print("Starting produtos extraction process...")
    
    # Create SQLAlchemy engine
    engine = create_engine(DATABASE_URL)
    
    # Read SQL query from file
    sql_file = Path(__file__).parent.parent.parent / "sql" / "extract" / "produtos.sql"
    with open(sql_file, 'r') as f:
        query = f.read()
    
    # Extract data from PostgreSQL
    print(f"Extracting produtos data from PostgreSQL...")
    df_produtos = pd.read_sql(query, engine)
    print(f"Extracted {len(df_produtos)} produtos records")
    
    # Save to Raw Layer as Parquet
    output_file = RAW_DATA_DIR / "produtos.parquet"
    df_produtos.to_parquet(output_file, index=False)
    print(f"Saved to {output_file}")
    
    print("Produtos extraction completed successfully!")


if __name__ == "__main__":
    extract_produtos()
