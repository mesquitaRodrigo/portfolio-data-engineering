"""
Transform script: Transform raw clientes data to dim_cliente in Curated Layer.
This script reads from Raw Layer and creates dimensional model in Curated Layer.
"""

import sys
from pathlib import Path

import pandas as pd

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent.parent))

from config.settings import RAW_DATA_DIR, DATA_DIR


def criar_dim_cliente():
    """
    Transform raw clientes data to dimensional model and save to Curated Layer.
    """
    print("Starting dim_cliente transformation process...")
    
    # Read raw data from Raw Layer
    raw_file = RAW_DATA_DIR / "clientes.parquet"
    print(f"Reading raw data from {raw_file}")
    df_raw = pd.read_parquet(raw_file)
    print(f"Loaded {len(df_raw)} raw clientes records")
    
    # Transform to dimensional model
    df_dim = df_raw.copy()
    df_dim = df_dim.rename(columns={
        'id': 'sk_cliente',
        'id': 'nk_cliente'
    })
    
    # Ensure proper column names for dimensional model
    df_dim['sk_cliente'] = df_dim['id']
    df_dim['nk_cliente'] = df_dim['id']
    
    # Add data warehouse load timestamp
    df_dim['dw_load_timestamp'] = pd.Timestamp.now()
    
    # Select and order columns
    columns = ['sk_cliente', 'nk_cliente', 'nome', 'cidade', 'email', 
               'telefone', 'data_cadastro', 'ativo', 'extract_timestamp', 
               'dw_load_timestamp']
    df_dim = df_dim[columns]
    
    # Save to Curated Layer as Parquet
    curated_dir = DATA_DIR / "curated"
    curated_dir.mkdir(parents=True, exist_ok=True)
    output_file = curated_dir / "dim_cliente.parquet"
    df_dim.to_parquet(output_file, index=False)
    print(f"Saved to {output_file}")
    
    print("Dim_cliente transformation completed successfully!")


if __name__ == "__main__":
    criar_dim_cliente()
