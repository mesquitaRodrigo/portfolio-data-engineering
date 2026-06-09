"""
Extract All Tables from ERP to Raw Layer
Sprint 2: ERP PostgreSQL → Raw Layer (Parquet)

This script extracts data from the ERP operational system (PostgreSQL)
and saves it to the Raw Layer as Parquet files without any transformations.
The Raw Layer serves as an immutable copy of the ERP data.
"""

import logging
import sys
from pathlib import Path
from typing import Dict, Tuple

import pandas as pd
from sqlalchemy import create_engine, text

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent.parent))
from config.settings import (
    DATABASE_URL,
    RAW_DATA_DIR,
    RAW_CLIENTES_FILE,
    RAW_PRODUTOS_FILE,
    RAW_PEDIDOS_FILE,
    RAW_ITENS_PEDIDO_FILE,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def connect_postgres() -> object:
    """
    Connect to PostgreSQL database using SQLAlchemy.
    
    Returns:
        SQLAlchemy engine object
        
    Raises:
        Exception: If connection fails
    """
    try:
        logger.info(f"Conectando ao PostgreSQL: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else DATABASE_URL}")
        engine = create_engine(DATABASE_URL)
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Conexão estabelecida com sucesso")
        return engine
    except Exception as e:
        logger.error(f"Erro ao conectar ao PostgreSQL: {e}")
        raise


def extract_table(engine: object, table_name: str) -> pd.DataFrame:
    """
    Extract data from a specific table in PostgreSQL.
    
    Args:
        engine: SQLAlchemy engine object
        table_name: Name of the table to extract
        
    Returns:
        DataFrame with the table data
        
    Raises:
        Exception: If extraction fails
    """
    try:
        logger.info(f"Extraindo tabela: {table_name}")
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, engine)
        logger.info(f"{len(df)} registros extraídos de {table_name}")
        return df
    except Exception as e:
        logger.error(f"Erro ao extrair tabela {table_name}: {e}")
        raise


def save_parquet(df: pd.DataFrame, file_path: Path, table_name: str) -> None:
    """
    Save DataFrame to Parquet file.
    
    Args:
        df: DataFrame to save
        file_path: Path where to save the Parquet file
        table_name: Name of the table (for logging)
        
    Raises:
        Exception: If save operation fails
    """
    try:
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save to Parquet using PyArrow engine
        df.to_parquet(file_path, engine='pyarrow', index=False)
        logger.info(f"Arquivo salvo: {file_path}")
    except Exception as e:
        logger.error(f"Erro ao salvar arquivo Parquet para {table_name}: {e}")
        raise


def main() -> None:
    """
    Main function to extract all tables from ERP to Raw Layer.
    
    This function:
    1. Connects to PostgreSQL
    2. Extracts all ERP tables
    3. Saves them as Parquet files
    4. Displays extraction statistics
    5. Handles errors gracefully
    """
    engine = None
    extraction_stats = {}
    
    try:
        # Connect to PostgreSQL
        engine = connect_postgres()
        
        # Define tables to extract
        tables = {
            'clientes': RAW_CLIENTES_FILE,
            'produtos': RAW_PRODUTOS_FILE,
            'pedidos': RAW_PEDIDOS_FILE,
            'itens_pedido': RAW_ITENS_PEDIDO_FILE,
        }
        
        logger.info("=" * 60)
        logger.info("Iniciando extração do ERP para Raw Layer")
        logger.info("=" * 60)
        
        # Extract each table
        for table_name, file_path in tables.items():
            try:
                df = extract_table(engine, table_name)
                save_parquet(df, file_path, table_name)
                extraction_stats[table_name] = len(df)
            except Exception as e:
                logger.error(f"Falha ao extrair tabela {table_name}: {e}")
                extraction_stats[table_name] = 0
        
        logger.info("=" * 60)
        logger.info("Extração concluída com sucesso")
        logger.info("=" * 60)
        
        # Display statistics
        display_statistics(extraction_stats)
        
    except Exception as e:
        logger.error(f"Erro fatal durante extração: {e}")
        sys.exit(1)
    finally:
        # Close connection
        if engine is not None:
            engine.dispose()
            logger.info("Conexão com PostgreSQL encerrada")


def display_statistics(stats: Dict[str, int]) -> None:
    """
    Display extraction statistics in a formatted table.
    
    Args:
        stats: Dictionary with table names and record counts
    """
    logger.info("")
    logger.info("Estatísticas de Extração")
    logger.info("-" * 40)
    logger.info(f"{'Tabela':<15} | {'Registros':<10}")
    logger.info("-" * 40)
    
    total_records = 0
    for table_name, count in stats.items():
        logger.info(f"{table_name:<15} | {count:<10}")
        total_records += count
    
    logger.info("-" * 40)
    logger.info(f"{'TOTAL':<15} | {total_records:<10}")
    logger.info("")
    logger.info(f"Arquivos salvos em: {RAW_DATA_DIR}")
    logger.info("")


if __name__ == "__main__":
    main()
