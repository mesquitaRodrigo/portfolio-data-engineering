"""
Transform script: Transform raw pedidos and itens_pedido data to fato_vendas in Curated Layer.
This script reads from Raw Layer and creates fact table in Curated Layer.
"""

import sys
from pathlib import Path

import pandas as pd

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent.parent))

from config.settings import RAW_DATA_DIR, DATA_DIR


def criar_fato_vendas():
    """
    Transform raw pedidos and itens_pedido data to fact table and save to Curated Layer.
    """
    print("Starting fato_vendas transformation process...")
    
    # Read raw data from Raw Layer
    pedidos_file = RAW_DATA_DIR / "pedidos.parquet"
    itens_file = RAW_DATA_DIR / "itens_pedido.parquet"
    
    print(f"Reading pedidos data from {pedidos_file}")
    df_pedidos = pd.read_parquet(pedidos_file)
    print(f"Loaded {len(df_pedidos)} pedidos records")
    
    print(f"Reading itens_pedido data from {itens_file}")
    df_itens = pd.read_parquet(itens_file)
    print(f"Loaded {len(df_itens)} itens_pedido records")
    
    # Join pedidos and itens_pedido
    print("Joining pedidos and itens_pedido...")
    df_fato = df_itens.merge(df_pedidos, on='id_pedido', how='inner')
    print(f"Joined to {len(df_fato)} fact records")
    
    # Transform to fact table model
    df_fato['sk_venda'] = df_fato['id_item']
    df_fato['nk_pedido'] = df_fato['id_pedido']
    df_fato['sk_produto'] = df_fato['id_produto']
    df_fato['sk_cliente'] = df_fato['id_cliente']
    df_fato['valor_total'] = df_fato['subtotal']
    df_fato['data_venda'] = df_fato['data_pedido']
    
    # Add data warehouse load timestamp
    df_fato['dw_load_timestamp'] = pd.Timestamp.now()
    
    # Select and order columns
    columns = ['sk_venda', 'nk_pedido', 'sk_produto', 'sk_cliente', 
               'quantidade', 'preco_unitario', 'valor_total', 'data_venda', 
               'status', 'extract_timestamp', 'dw_load_timestamp']
    df_fato = df_fato[columns]
    
    # Save to Curated Layer as Parquet
    curated_dir = DATA_DIR / "curated"
    curated_dir.mkdir(parents=True, exist_ok=True)
    output_file = curated_dir / "fato_vendas.parquet"
    df_fato.to_parquet(output_file, index=False)
    print(f"Saved to {output_file}")
    
    print("Fato_vendas transformation completed successfully!")


if __name__ == "__main__":
    criar_fato_vendas()
