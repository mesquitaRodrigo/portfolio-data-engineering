"""
ETL Script to build the Curated Layer (Mini Data Warehouse)
Transforms Raw Layer data into a dimensional model for analytics.

Architecture: ERP PostgreSQL → Raw Layer → Curated Layer → DuckDB → Analytics
"""

import pandas as pd
import os
from pathlib import Path


def create_dim_cliente():
    """
    Create dim_cliente dimension table.
    
    Source: data/raw/clientes.parquet
    Target: data/curated/dim_cliente.parquet
    
    Fields: id_cliente, nome, cidade
    """
    print("[INFO] Creating dim_cliente...")
    
    # Read from raw layer
    df = pd.read_parquet('data/raw/clientes.parquet')
    
    # Select and rename columns
    dim_cliente = df[['id_cliente', 'nome', 'cidade']].copy()
    
    # Ensure output directory exists
    output_dir = Path('data/curated')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Write to curated layer
    dim_cliente.to_parquet('data/curated/dim_cliente.parquet', index=False)
    
    print(f"[INFO] dim_cliente: {len(dim_cliente)} registros")
    return dim_cliente


def create_dim_produto():
    """
    Create dim_produto dimension table.
    
    Source: data/raw/produtos.parquet
    Target: data/curated/dim_produto.parquet
    
    Fields: id_produto, nome, categoria, preco
    """
    print("[INFO] Creating dim_produto...")
    
    # Read from raw layer
    df = pd.read_parquet('data/raw/produtos.parquet')
    
    # Select and rename columns
    dim_produto = df[['id_produto', 'nome', 'categoria', 'preco']].copy()
    
    # Ensure output directory exists
    output_dir = Path('data/curated')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Write to curated layer
    dim_produto.to_parquet('data/curated/dim_produto.parquet', index=False)
    
    print(f"[INFO] dim_produto: {len(dim_produto)} registros")
    return dim_produto


def create_dim_data():
    """
    Create dim_data dimension table.
    
    Source: data/raw/pedidos.parquet (extract unique dates)
    Target: data/curated/dim_data.parquet
    
    Fields: data, ano, mes, dia, trimestre, nome_mes
    """
    print("[INFO] Creating dim_data...")
    
    # Read from raw layer
    df = pd.read_parquet('data/raw/pedidos.parquet')
    
    # Extract unique dates
    dates = df['data_pedido'].drop_duplicates().sort_values().copy()
    
    # Create dimension table
    dim_data = pd.DataFrame({'data': dates})
    
    # Convert to datetime if not already
    dim_data['data'] = pd.to_datetime(dim_data['data'])
    
    # Extract date components
    dim_data['ano'] = dim_data['data'].dt.year
    dim_data['mes'] = dim_data['data'].dt.month
    dim_data['dia'] = dim_data['data'].dt.day
    dim_data['trimestre'] = dim_data['data'].dt.quarter
    
    # Add month names in Portuguese
    month_names = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }
    dim_data['nome_mes'] = dim_data['mes'].map(month_names)
    
    # Ensure output directory exists
    output_dir = Path('data/curated')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Write to curated layer
    dim_data.to_parquet('data/curated/dim_data.parquet', index=False)
    
    print(f"[INFO] dim_data: {len(dim_data)} registros")
    return dim_data


def create_fato_vendas():
    """
    Create fato_vendas fact table.
    
    Source: data/raw/pedidos.parquet + data/raw/itens_pedido.parquet
    Target: data/curated/fato_vendas.parquet
    
    Fields: id_pedido, data_pedido, id_cliente, id_produto, quantidade, 
            preco_unitario, valor_total
    
    Calculation: valor_total = quantidade * preco_unitario
    """
    print("[INFO] Creating fato_vendas...")
    
    # Read from raw layer
    pedidos = pd.read_parquet('data/raw/pedidos.parquet')
    itens_pedido = pd.read_parquet('data/raw/itens_pedido.parquet')
    
    # Join pedidos with itens_pedido
    fato_vendas = pd.merge(
        pedidos[['id_pedido', 'id_cliente', 'data_pedido']],
        itens_pedido[['id_pedido', 'id_produto', 'quantidade', 'preco_unitario']],
        on='id_pedido',
        how='inner'
    )
    
    # Calculate valor_total
    fato_vendas['valor_total'] = fato_vendas['quantidade'] * fato_vendas['preco_unitario']
    
    # Select and order columns
    fato_vendas = fato_vendas[[
        'id_pedido', 'data_pedido', 'id_cliente', 'id_produto',
        'quantidade', 'preco_unitario', 'valor_total'
    ]].copy()
    
    # Ensure output directory exists
    output_dir = Path('data/curated')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Write to curated layer
    fato_vendas.to_parquet('data/curated/fato_vendas.parquet', index=False)
    
    print(f"[INFO] fato_vendas: {len(fato_vendas)} registros")
    return fato_vendas


def main():
    """
    Main function to build the entire Curated Layer.
    """
    print("=" * 60)
    print("Building Curated Layer (Mini Data Warehouse)")
    print("=" * 60)
    print()
    
    # Create all dimension and fact tables
    create_dim_cliente()
    create_dim_produto()
    create_dim_data()
    create_fato_vendas()
    
    print()
    print("=" * 60)
    print("Curated Layer built successfully!")
    print("=" * 60)
    print()
    print("Generated files:")
    print("  - data/curated/dim_cliente.parquet")
    print("  - data/curated/dim_produto.parquet")
    print("  - data/curated/dim_data.parquet")
    print("  - data/curated/fato_vendas.parquet")
    print()


if __name__ == "__main__":
    main()
