"""
Pipeline Monitor
Tracks pipeline execution metrics and stores execution history.

This module provides comprehensive monitoring capabilities:
- Execution start/end time tracking
- Duration calculation
- Status recording
- Records processed counting
- CSV and PostgreSQL persistence
"""

import logging
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import csv

import pandas as pd
from sqlalchemy import create_engine, text

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent))
from config.settings import DATABASE_URL
from config.logging_config import get_monitor_logger, log_success, log_error

# Configure logger
logger = get_monitor_logger()

# Execution history CSV path
EXECUTION_HISTORY_CSV = Path('monitoring/execution_history.csv')


class PipelineMonitor:
    """
    Monitors pipeline execution and stores metrics.
    
    Tracks:
    - Execution ID (UUID)
    - Start time
    - End time
    - Duration
    - Status
    - Records processed
    - Layer (extract, curated, analytics, quality, tests)
    """
    
    def __init__(self):
        self.execution_id: str = str(uuid.uuid4())
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.duration_seconds: Optional[float] = None
        self.status: str = 'pending'
        self.records_processed: int = 0
        self.layer: str = 'unknown'
        self.engine = None
        self.execution_data: Dict[str, Any] = {}
    
    def start_execution(self, layer: str) -> None:
        """
        Start monitoring a pipeline execution.
        
        Args:
            layer: Pipeline layer being executed (extract, curated, analytics, quality, tests)
        """
        self.execution_id = str(uuid.uuid4())
        self.start_time = datetime.now()
        self.layer = layer
        self.status = 'running'
        self.records_processed = 0
        
        logger.info(f"Starting execution {self.execution_id} for layer: {layer}")
        logger.info(f"Start time: {self.start_time}")
        
        # Store execution data
        self.execution_data = {
            'execution_id': self.execution_id,
            'layer': layer,
            'start_time': self.start_time,
            'status': self.status,
            'records_processed': self.records_processed
        }
    
    def end_execution(self, records_processed: int = 0, status: str = 'success') -> None:
        """
        End monitoring a pipeline execution.
        
        Args:
            records_processed: Number of records processed
            status: Execution status (success, failed, partial)
        """
        self.end_time = datetime.now()
        self.records_processed = records_processed
        self.status = status
        
        # Calculate duration
        if self.start_time:
            self.duration_seconds = (self.end_time - self.start_time).total_seconds()
        
        logger.info(f"Ending execution {self.execution_id}")
        logger.info(f"End time: {self.end_time}")
        logger.info(f"Duration: {self.duration_seconds:.2f} seconds")
        logger.info(f"Records processed: {self.records_processed}")
        logger.info(f"Status: {self.status}")
        
        # Update execution data
        self.execution_data.update({
            'end_time': self.end_time,
            'duration_seconds': self.duration_seconds,
            'records_processed': self.records_processed,
            'status': self.status
        })
        
        # Save to CSV and PostgreSQL
        self.save_to_csv()
        self.save_to_postgresql()
    
    def save_to_csv(self) -> None:
        """Save execution data to CSV file."""
        try:
            # Ensure directory exists
            EXECUTION_HISTORY_CSV.parent.mkdir(parents=True, exist_ok=True)
            
            # Check if file exists to determine if we need headers
            file_exists = EXECUTION_HISTORY_CSV.exists()
            
            # Prepare data for CSV
            csv_data = {
                'execution_id': self.execution_id,
                'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S') if self.start_time else '',
                'end_time': self.end_time.strftime('%Y-%m-%d %H:%M:%S') if self.end_time else '',
                'duration_seconds': self.duration_seconds if self.duration_seconds else 0,
                'status': self.status,
                'records_processed': self.records_processed,
                'layer': self.layer
            }
            
            # Write to CSV
            with open(EXECUTION_HISTORY_CSV, 'a', newline='') as csvfile:
                fieldnames = ['execution_id', 'start_time', 'end_time', 'duration_seconds', 
                             'status', 'records_processed', 'layer']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader()
                
                writer.writerow(csv_data)
            
            log_success(logger, f"Execution saved to CSV: {EXECUTION_HISTORY_CSV}")
            
        except Exception as e:
            log_error(logger, "Failed to save execution to CSV", e)
    
    def save_to_postgresql(self) -> None:
        """Save execution data to PostgreSQL audit table."""
        try:
            # Connect to PostgreSQL
            self.engine = create_engine(DATABASE_URL)
            
            with self.engine.connect() as conn:
                # Insert into audit.pipeline_execution
                insert_query = text("""
                    INSERT INTO audit.pipeline_execution 
                    (id_execucao, inicio_execucao, fim_execucao, duracao_segundos, 
                     status, registros_processados, camada)
                    VALUES (:id_execucao, :inicio_execucao, :fim_execucao, :duracao_segundos,
                            :status, :registros_processados, :camada)
                """)
                
                conn.execute(insert_query, {
                    'id_execucao': self.execution_id,
                    'inicio_execucao': self.start_time,
                    'fim_execucao': self.end_time,
                    'duracao_segundos': self.duration_seconds,
                    'status': self.status,
                    'registros_processados': self.records_processed,
                    'camada': self.layer
                })
                
                conn.commit()
            
            log_success(logger, f"Execution saved to PostgreSQL audit table")
            
        except Exception as e:
            log_error(logger, "Failed to save execution to PostgreSQL", e)
        finally:
            if self.engine:
                self.engine.dispose()
    
    def get_execution_history(self, limit: int = 100) -> pd.DataFrame:
        """
        Retrieve execution history from CSV.
        
        Args:
            limit: Maximum number of records to retrieve
            
        Returns:
            DataFrame with execution history
        """
        try:
            if EXECUTION_HISTORY_CSV.exists():
                df = pd.read_csv(EXECUTION_HISTORY_CSV)
                df['start_time'] = pd.to_datetime(df['start_time'])
                df['end_time'] = pd.to_datetime(df['end_time'])
                return df.tail(limit)
            else:
                logger.warning(f"Execution history CSV not found: {EXECUTION_HISTORY_CSV}")
                return pd.DataFrame()
        except Exception as e:
            log_error(logger, "Failed to read execution history from CSV", e)
            return pd.DataFrame()
    
    def get_execution_history_from_db(self, limit: int = 100) -> pd.DataFrame:
        """
        Retrieve execution history from PostgreSQL.
        
        Args:
            limit: Maximum number of records to retrieve
            
        Returns:
            DataFrame with execution history
        """
        try:
            self.engine = create_engine(DATABASE_URL)
            
            with self.engine.connect() as conn:
                query = text("""
                    SELECT id_execucao, inicio_execucao, fim_execucao, 
                           duracao_segundos, status, registros_processados, camada
                    FROM audit.pipeline_execution
                    ORDER BY inicio_execucao DESC
                    LIMIT :limit
                """)
                
                df = pd.read_sql(query, conn, params={'limit': limit})
            
            return df
            
        except Exception as e:
            log_error(logger, "Failed to read execution history from PostgreSQL", e)
            return pd.DataFrame()
        finally:
            if self.engine:
                self.engine.dispose()
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """
        Get summary statistics of pipeline executions.
        
        Returns:
            Dictionary with summary statistics
        """
        try:
            df = self.get_execution_history_from_db()
            
            if df.empty:
                return {
                    'total_executions': 0,
                    'successful_executions': 0,
                    'failed_executions': 0,
                    'avg_duration_seconds': 0,
                    'total_records_processed': 0
                }
            
            stats = {
                'total_executions': len(df),
                'successful_executions': len(df[df['status'] == 'success']),
                'failed_executions': len(df[df['status'] == 'failed']),
                'avg_duration_seconds': df['duracao_segundos'].mean(),
                'total_records_processed': df['registros_processados'].sum()
            }
            
            return stats
            
        except Exception as e:
            log_error(logger, "Failed to calculate summary statistics", e)
            return {}


def monitor_pipeline_execution(layer: str, execution_func, *args, **kwargs) -> Any:
    """
    Decorator/context manager to monitor pipeline execution.
    
    Args:
        layer: Pipeline layer being executed
        execution_func: Function to execute
        *args: Arguments to pass to execution function
        **kwargs: Keyword arguments to pass to execution function
        
    Returns:
        Result of execution function
    """
    monitor = PipelineMonitor()
    
    try:
        monitor.start_execution(layer)
        result = execution_func(*args, **kwargs)
        monitor.end_execution(status='success')
        return result
    except Exception as e:
        monitor.end_execution(status='failed')
        log_error(logger, f"Pipeline execution failed for layer: {layer}", e)
        raise


def main():
    """Main function to demonstrate pipeline monitoring."""
    logger.info("=" * 60)
    logger.info("Pipeline Monitor Demo")
    logger.info("=" * 60)
    
    # Example usage
    monitor = PipelineMonitor()
    monitor.start_execution('extract')
    
    # Simulate some work
    import time
    time.sleep(2)
    
    monitor.end_execution(records_processed=1000, status='success')
    
    # Get execution history
    history = monitor.get_execution_history()
    logger.info(f"\nExecution History:\n{history}")
    
    # Get summary stats
    stats = monitor.get_summary_stats()
    logger.info(f"\nSummary Statistics:\n{stats}")


if __name__ == "__main__":
    main()
