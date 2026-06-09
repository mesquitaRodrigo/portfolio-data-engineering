"""
Load script: Load Curated Layer data into DuckDB for analytics.
This script sets up DuckDB to query Parquet files from the Curated Layer.
"""

import sys
from pathlib import Path

import duckdb

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent.parent))

from config.settings import DATA_DIR


def load_duckdb():
    """
    Load Curated Layer Parquet files into DuckDB for analytics.
    This creates views for each table in the Curated Layer.
    """
    print("Starting DuckDB load process...")
    
    # Initialize DuckDB connection
    con = duckdb.connect(database=':memory:')
    
    # Define paths to Curated Layer files
    curated_dir = DATA_DIR / "curated"
    dim_cliente_path = curated_dir / "dim_cliente.parquet"
    dim_produto_path = curated_dir / "dim_produto.parquet"
    fato_vendas_path = curated_dir / "fato_vendas.parquet"
    
    # Create views in DuckDB
    print(f"Creating dim_cliente view from {dim_cliente_path}")
    con.execute(f"""
        CREATE OR REPLACE VIEW dim_cliente AS 
        SELECT * FROM read_parquet('{dim_cliente_path}')
    """)
    
    print(f"Creating dim_produto view from {dim_produto_path}")
    con.execute(f"""
        CREATE OR REPLACE VIEW dim_produto AS 
        SELECT * FROM read_parquet('{dim_produto_path}')
    """)
    
    print(f"Creating fato_vendas view from {fato_vendas_path}")
    con.execute(f"""
        CREATE OR REPLACE VIEW fato_vendas AS 
        SELECT * FROM read_parquet('{fato_vendas_path}')
    """)
    
    # Verify the views were created
    print("\nVerifying views...")
    result = con.execute("SHOW TABLES").fetchall()
    print(f"Available views: {[row[0] for row in result]}")
    
    # Test a simple query
    print("\nTesting query on fato_vendas...")
    test_result = con.execute("SELECT COUNT(*) as total_records FROM fato_vendas").fetchone()
    print(f"Total records in fato_vendas: {test_result[0]}")
    
    print("\nDuckDB load completed successfully!")
    print("You can now query the views using DuckDB.")
    
    # Return connection for use in analytics scripts
    return con


if __name__ == "__main__":
    con = load_duckdb()
    
    # Keep connection open for interactive use
    print("\nDuckDB connection is active. Press Ctrl+C to exit.")
    try:
        while True:
            query = input("\nEnter SQL query (or 'exit' to quit): ")
            if query.lower() == 'exit':
                break
            try:
                result = con.execute(query).fetchdf()
                print(result)
            except Exception as e:
                print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        con.close()
