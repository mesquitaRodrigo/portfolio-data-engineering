"""
Data Quality Metrics Generator
Calculates and stores data quality metrics for dashboard visualization.

This script calculates quality metrics across all pipeline layers:
- Total records per entity (clientes, produtos, pedidos, itens)
- Null percentage
- Duplicate percentage
- Data integrity percentage
- Execution timestamp
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import pandas as pd

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent))
from config.settings import (
    RAW_DATA_DIR,
    CURATED_DATA_DIR,
    RAW_CLIENTES_FILE,
    RAW_PRODUTOS_FILE,
    RAW_PEDIDOS_FILE,
    RAW_ITENS_PEDIDO_FILE,
    CURATED_DIM_CLIENTE_FILE,
    CURATED_DIM_PRODUTO_FILE,
    CURATED_FATO_VENDAS_FILE,
    ANALYTICS_DATA_DIR,
)
from config.logging_config import get_analytics_logger, log_success, log_error

# Configure logger
logger = get_analytics_logger()

# Output file
DATA_QUALITY_METRICS_FILE = ANALYTICS_DATA_DIR / 'data_quality_metrics.parquet'


def calculate_null_percentage(df: pd.DataFrame, columns: list) -> float:
    """
    Calculate the percentage of null values in specified columns.
    
    Args:
        df: DataFrame to analyze
        columns: List of columns to check for nulls
        
    Returns:
        Percentage of null values (0-100)
    """
    if df.empty:
        return 0.0
    
    total_cells = len(df) * len(columns)
    null_cells = df[columns].isnull().sum().sum()
    
    return (null_cells / total_cells) * 100 if total_cells > 0 else 0.0


def calculate_duplicate_percentage(df: pd.DataFrame, key_columns: list) -> float:
    """
    Calculate the percentage of duplicate records based on key columns.
    
    Args:
        df: DataFrame to analyze
        key_columns: Columns to use for duplicate detection
        
    Returns:
        Percentage of duplicates (0-100)
    """
    if df.empty:
        return 0.0
    
    total_records = len(df)
    duplicates = df.duplicated(subset=key_columns, keep=False).sum()
    
    return (duplicates / total_records) * 100 if total_records > 0 else 0.0


def calculate_integrity_percentage(raw_df: pd.DataFrame, curated_df: pd.DataFrame) -> float:
    """
    Calculate data integrity percentage between raw and curated layers.
    
    Args:
        raw_df: Raw layer DataFrame
        curated_df: Curated layer DataFrame
        
    Returns:
        Integrity percentage (0-100)
    """
    if raw_df.empty or curated_df.empty:
        return 0.0
    
    raw_count = len(raw_df)
    curated_count = len(curated_df)
    
    # Integrity is based on record count match
    if raw_count == curated_count:
        return 100.0
    else:
        return (min(raw_count, curated_count) / max(raw_count, curated_count)) * 100


def calculate_raw_layer_metrics() -> Dict[str, Any]:
    """
    Calculate quality metrics for Raw Layer.
    
    Returns:
        Dictionary with raw layer metrics
    """
    metrics = {}
    
    try:
        # Clientes
        if RAW_CLIENTES_FILE.exists():
            df = pd.read_parquet(RAW_CLIENTES_FILE)
            metrics['total_clientes'] = len(df)
            metrics['percentual_nulos_clientes'] = calculate_null_percentage(
                df, ['id_cliente', 'nome', 'cidade']
            )
            metrics['percentual_duplicados_clientes'] = calculate_duplicate_percentage(
                df, ['id_cliente']
            )
        else:
            metrics['total_clientes'] = 0
            metrics['percentual_nulos_clientes'] = 0
            metrics['percentual_duplicados_clientes'] = 0
        
        # Produtos
        if RAW_PRODUTOS_FILE.exists():
            df = pd.read_parquet(RAW_PRODUTOS_FILE)
            metrics['total_produtos'] = len(df)
            metrics['percentual_nulos_produtos'] = calculate_null_percentage(
                df, ['id_produto', 'nome', 'categoria', 'preco']
            )
            metrics['percentual_duplicados_produtos'] = calculate_duplicate_percentage(
                df, ['id_produto']
            )
        else:
            metrics['total_produtos'] = 0
            metrics['percentual_nulos_produtos'] = 0
            metrics['percentual_duplicados_produtos'] = 0
        
        # Pedidos
        if RAW_PEDIDOS_FILE.exists():
            df = pd.read_parquet(RAW_PEDIDOS_FILE)
            metrics['total_pedidos'] = len(df)
            metrics['percentual_nulos_pedidos'] = calculate_null_percentage(
                df, ['id_pedido', 'id_cliente', 'data_pedido']
            )
            metrics['percentual_duplicados_pedidos'] = calculate_duplicate_percentage(
                df, ['id_pedido']
            )
        else:
            metrics['total_pedidos'] = 0
            metrics['percentual_nulos_pedidos'] = 0
            metrics['percentual_duplicados_pedidos'] = 0
        
        # Itens Pedido
        if RAW_ITENS_PEDIDO_FILE.exists():
            df = pd.read_parquet(RAW_ITENS_PEDIDO_FILE)
            metrics['total_itens'] = len(df)
            metrics['percentual_nulos_itens'] = calculate_null_percentage(
                df, ['id_item', 'id_pedido', 'id_produto', 'quantidade', 'preco_unitario']
            )
            metrics['percentual_duplicados_itens'] = calculate_duplicate_percentage(
                df, ['id_item']
            )
        else:
            metrics['total_itens'] = 0
            metrics['percentual_nulos_itens'] = 0
            metrics['percentual_duplicados_itens'] = 0
        
        log_success(logger, "Raw layer metrics calculated")
        
    except Exception as e:
        log_error(logger, "Failed to calculate raw layer metrics", e)
        # Return default values on error
        metrics = {
            'total_clientes': 0,
            'total_produtos': 0,
            'total_pedidos': 0,
            'total_itens': 0,
            'percentual_nulos_clientes': 0,
            'percentual_nulos_produtos': 0,
            'percentual_nulos_pedidos': 0,
            'percentual_nulos_itens': 0,
            'percentual_duplicados_clientes': 0,
            'percentual_duplicados_produtos': 0,
            'percentual_duplicados_pedidos': 0,
            'percentual_duplicados_itens': 0,
        }
    
    return metrics


def calculate_curated_layer_metrics() -> Dict[str, Any]:
    """
    Calculate quality metrics for Curated Layer.
    
    Returns:
        Dictionary with curated layer metrics
    """
    metrics = {}
    
    try:
        # Calculate integrity percentages
        if RAW_CLIENTES_FILE.exists() and CURATED_DIM_CLIENTE_FILE.exists():
            raw_df = pd.read_parquet(RAW_CLIENTES_FILE)
            curated_df = pd.read_parquet(CURATED_DIM_CLIENTE_FILE)
            metrics['percentual_integridade_cliente'] = calculate_integrity_percentage(raw_df, curated_df)
        else:
            metrics['percentual_integridade_cliente'] = 0
        
        if RAW_PRODUTOS_FILE.exists() and CURATED_DIM_PRODUTO_FILE.exists():
            raw_df = pd.read_parquet(RAW_PRODUTOS_FILE)
            curated_df = pd.read_parquet(CURATED_DIM_PRODUTO_FILE)
            metrics['percentual_integridade_produto'] = calculate_integrity_percentage(raw_df, curated_df)
        else:
            metrics['percentual_integridade_produto'] = 0
        
        # Fato vendas integrity (based on raw pedidos + itens_pedido)
        if RAW_PEDIDOS_FILE.exists() and RAW_ITENS_PEDIDO_FILE.exists() and CURATED_FATO_VENDAS_FILE.exists():
            raw_pedidos = pd.read_parquet(RAW_PEDIDOS_FILE)
            raw_itens = pd.read_parquet(RAW_ITENS_PEDIDO_FILE)
            curated_fato = pd.read_parquet(CURATED_FATO_VENDAS_FILE)
            expected_count = len(raw_itens)
            actual_count = len(curated_fato)
            metrics['percentual_integridade_fato'] = (actual_count / expected_count) * 100 if expected_count > 0 else 0
        else:
            metrics['percentual_integridade_fato'] = 0
        
        # Overall integrity (average of all integrity metrics)
        integrity_values = [
            metrics.get('percentual_integridade_cliente', 0),
            metrics.get('percentual_integridade_produto', 0),
            metrics.get('percentual_integridade_fato', 0)
        ]
        metrics['percentual_integridade_geral'] = sum(integrity_values) / len(integrity_values) if integrity_values else 0
        
        log_success(logger, "Curated layer metrics calculated")
        
    except Exception as e:
        log_error(logger, "Failed to calculate curated layer metrics", e)
        metrics = {
            'percentual_integridade_cliente': 0,
            'percentual_integridade_produto': 0,
            'percentual_integridade_fato': 0,
            'percentual_integridade_geral': 0,
        }
    
    return metrics


def generate_data_quality_metrics() -> pd.DataFrame:
    """
    Generate comprehensive data quality metrics.
    
    Returns:
        DataFrame with data quality metrics
    """
    logger.info("=" * 60)
    logger.info("Generating Data Quality Metrics")
    logger.info("=" * 60)
    
    # Calculate metrics for each layer
    raw_metrics = calculate_raw_layer_metrics()
    curated_metrics = calculate_curated_layer_metrics()
    
    # Combine all metrics
    all_metrics = {**raw_metrics, **curated_metrics}
    
    # Add execution timestamp
    all_metrics['data_execucao'] = datetime.now()
    
    # Create DataFrame
    df = pd.DataFrame([all_metrics])
    
    # Ensure output directory exists
    ANALYTICS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save to Parquet
    df.to_parquet(DATA_QUALITY_METRICS_FILE, index=False)
    
    log_success(logger, f"Data quality metrics saved to {DATA_QUALITY_METRICS_FILE}")
    
    # Print summary
    logger.info("")
    logger.info("Data Quality Metrics Summary:")
    logger.info("-" * 40)
    logger.info(f"Total Clientes: {all_metrics.get('total_clientes', 0)}")
    logger.info(f"Total Produtos: {all_metrics.get('total_produtos', 0)}")
    logger.info(f"Total Pedidos: {all_metrics.get('total_pedidos', 0)}")
    logger.info(f"Total Itens: {all_metrics.get('total_itens', 0)}")
    logger.info(f"Integridade Geral: {all_metrics.get('percentual_integridade_geral', 0):.2f}%")
    logger.info("-" * 40)
    
    return df


def main():
    """Main function to generate data quality metrics."""
    try:
        generate_data_quality_metrics()
        logger.info("")
        logger.info("=" * 60)
        logger.info("Data Quality Metrics Generation Completed")
        logger.info("=" * 60)
    except Exception as e:
        log_error(logger, "Failed to generate data quality metrics", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
