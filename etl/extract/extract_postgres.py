"""
Extract script: Load data from CSV and insert into PostgreSQL database.
This script reads the raw CSV file and loads it into the PostgreSQL database.
"""

import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent.parent))

from config.settings import DATABASE_URL, RAW_SALES_FILE


def extract_and_load_to_postgres():
    """
    Read CSV data and load into PostgreSQL database.
    Creates sample data for clientes and produtos tables if they don't exist.
    """
    print("Starting extraction process...")
    
    # Create SQLAlchemy engine
    engine = create_engine(DATABASE_URL)
    
    # Read the sales CSV data
    print(f"Reading sales data from {RAW_SALES_FILE}")
    df_sales = pd.read_csv(RAW_SALES_FILE)
    print(f"Loaded {len(df_sales)} sales records")
    
    # Load data into PostgreSQL
    with engine.begin() as connection:
        # Insert sample clientes data
        print("Inserting sample clientes data...")
        clientes_data = [
            (1, "João Silva", "São Paulo"),
            (2, "Maria Santos", "Rio de Janeiro"),
            (3, "Pedro Oliveira", "Belo Horizonte"),
            (4, "Ana Costa", "Curitiba"),
            (5, "Carlos Lima", "Porto Alegre")
        ]
        
        for cliente in clientes_data:
            connection.execute(
                text("INSERT INTO clientes (id, nome, cidade) VALUES (:id, :nome, :cidade) "
                     "ON CONFLICT (id) DO NOTHING"),
                {"id": cliente[0], "nome": cliente[1], "cidade": cliente[2]}
            )
        
        # Insert sample produtos data
        print("Inserting sample produtos data...")
        produtos_data = [
            (1, "Notebook Dell", "Eletrônicos", 3500.00),
            (2, "Mouse Logitech", "Acessórios", 80.00),
            (3, "Monitor Samsung", "Eletrônicos", 1200.00),
            (4, "Teclado Mecânico", "Acessórios", 150.00)
        ]
        
        for produto in produtos_data:
            connection.execute(
                text("INSERT INTO produtos (id_produto, nome, categoria, preco) "
                     "VALUES (:id_produto, :nome, :categoria, :preco) "
                     "ON CONFLICT (id_produto) DO NOTHING"),
                {"id_produto": produto[0], "nome": produto[1], 
                 "categoria": produto[2], "preco": produto[3]}
            )
        
        # Insert sales data
        print("Inserting sales data...")
        df_sales.to_sql('vendas', connection, if_exists='append', index=False)
    
    print("Extraction and loading completed successfully!")
    print(f"Total sales records inserted: {len(df_sales)}")


if __name__ == "__main__":
    extract_and_load_to_postgres()
