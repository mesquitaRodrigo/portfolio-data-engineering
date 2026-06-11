"""
Pipeline Orchestration Script
Executes the complete data pipeline: Extract → Curated → Load DW → Analytics → Tests

This script orchestrates the execution of the entire data engineering pipeline:
1. Extract: Extract data from PostgreSQL ERP to Raw Layer
2. Curated: Transform Raw Layer to Curated Layer (Dimensional Model)
3. Load DW: Load Curated Layer to PostgreSQL Data Warehouse
4. Analytics: Calculate business metrics from Curated Layer
5. Tests: Run comprehensive tests to validate all layers

All steps are executed in sequence with proper error handling, logging, and monitoring.
"""

import sys
import subprocess
from pathlib import Path
import logging

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent))

from config.logging_config import get_pipeline_logger, log_success, log_error
from monitoring.pipeline_monitor import PipelineMonitor

# Configure logger
logger = get_pipeline_logger()


class PipelineOrchestrator:
    """Orchestrates the complete data pipeline execution"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.steps_completed = []
        self.steps_failed = []
    
    def run_extract(self) -> bool:
        """Execute Extract step: ERP → Raw Layer"""
        logger.info("")
        logger.info("=" * 70)
        logger.info("PASSO 1: EXTRACT - ERP → RAW LAYER")
        logger.info("=" * 70)
        logger.info("")
        
        monitor = PipelineMonitor()
        monitor.start_execution('extract')
        
        try:
            extract_script = self.project_dir / "etl" / "extract" / "extract_all_tables.py"
            logger.info(f"Executando: {extract_script}")
            
            result = subprocess.run(
                [sys.executable, str(extract_script)],
                cwd=str(self.project_dir),
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info("✓ Extract concluído com sucesso")
                self.steps_completed.append("Extract")
                monitor.end_execution(status='success')
                return True
            else:
                logger.error(f"✗ Extract falhou: {result.stderr}")
                self.steps_failed.append("Extract")
                monitor.end_execution(status='failed')
                return False
                
        except Exception as e:
            logger.error(f"✗ Erro ao executar Extract: {e}")
            self.steps_failed.append("Extract")
            monitor.end_execution(status='failed')
            return False
    
    def run_curated(self) -> bool:
        """Execute Curated step: Raw Layer → Curated Layer"""
        logger.info("")
        logger.info("=" * 70)
        logger.info("PASSO 2: CURATED - RAW LAYER → CURATED LAYER")
        logger.info("=" * 70)
        logger.info("")
        
        monitor = PipelineMonitor()
        monitor.start_execution('curated')
        
        try:
            curated_script = self.project_dir / "etl" / "transform" / "build_curated_layer.py"
            logger.info(f"Executando: {curated_script}")
            
            result = subprocess.run(
                [sys.executable, str(curated_script)],
                cwd=str(self.project_dir),
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info("✓ Curated concluído com sucesso")
                self.steps_completed.append("Curated")
                monitor.end_execution(status='success')
                return True
            else:
                logger.error(f"✗ Curated falhou: {result.stderr}")
                self.steps_failed.append("Curated")
                monitor.end_execution(status='failed')
                return False
                
        except Exception as e:
            logger.error(f"✗ Erro ao executar Curated: {e}")
            self.steps_failed.append("Curated")
            monitor.end_execution(status='failed')
            return False
    
    def run_load_dw(self) -> bool:
        """Execute Load DW step: Curated Layer → PostgreSQL Data Warehouse"""
        logger.info("")
        logger.info("=" * 70)
        logger.info("PASSO 3: LOAD DW - CURATED LAYER → POSTGRESQL DW")
        logger.info("=" * 70)
        logger.info("")
        
        monitor = PipelineMonitor()
        monitor.start_execution('load_dw')
        
        try:
            load_dw_script = self.project_dir / "etl" / "load" / "load_dw_postgres.py"
            logger.info(f"Executando: {load_dw_script}")
            
            result = subprocess.run(
                [sys.executable, str(load_dw_script)],
                cwd=str(self.project_dir),
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info("✓ Load DW concluído com sucesso")
                self.steps_completed.append("Load DW")
                monitor.end_execution(status='success')
                return True
            else:
                logger.error(f"✗ Load DW falhou: {result.stderr}")
                self.steps_failed.append("Load DW")
                monitor.end_execution(status='failed')
                return False
                
        except Exception as e:
            logger.error(f"✗ Erro ao executar Load DW: {e}")
            self.steps_failed.append("Load DW")
            monitor.end_execution(status='failed')
            return False
    
    def run_analytics(self) -> bool:
        """Execute Analytics step: Curated Layer → Analytics Layer"""
        logger.info("")
        logger.info("=" * 70)
        logger.info("PASSO 4: ANALYTICS - CURATED LAYER → ANALYTICS LAYER")
        logger.info("=" * 70)
        logger.info("")
        
        monitor = PipelineMonitor()
        monitor.start_execution('analytics')
        
        try:
            analytics_script = self.project_dir / "analytics" / "run_analytics.py"
            logger.info(f"Executando: {analytics_script}")
            
            result = subprocess.run(
                [sys.executable, str(analytics_script)],
                cwd=str(self.project_dir),
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info("✓ Analytics concluído com sucesso")
                self.steps_completed.append("Analytics")
                monitor.end_execution(status='success')
                return True
            else:
                logger.error(f"✗ Analytics falhou: {result.stderr}")
                self.steps_failed.append("Analytics")
                monitor.end_execution(status='failed')
                return False
                
        except Exception as e:
            logger.error(f"✗ Erro ao executar Analytics: {e}")
            self.steps_failed.append("Analytics")
            monitor.end_execution(status='failed')
            return False
    
    def run_tests(self) -> bool:
        """Execute Tests step: Validate all layers"""
        logger.info("")
        logger.info("=" * 70)
        logger.info("PASSO 5: TESTES - VALIDAÇÃO DE TODAS AS CAMADAS")
        logger.info("=" * 70)
        logger.info("")
        
        monitor = PipelineMonitor()
        monitor.start_execution('tests')
        
        try:
            test_script = self.project_dir / "test_project.py"
            logger.info(f"Executando: {test_script}")
            
            result = subprocess.run(
                [sys.executable, str(test_script)],
                cwd=str(self.project_dir),
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info("✓ Testes concluídos com sucesso")
                self.steps_completed.append("Testes")
                monitor.end_execution(status='success')
                return True
            else:
                logger.error(f"✗ Testes falharam: {result.stderr}")
                self.steps_failed.append("Testes")
                monitor.end_execution(status='failed')
                return False
                
        except Exception as e:
            logger.error(f"✗ Erro ao executar Testes: {e}")
            self.steps_failed.append("Testes")
            monitor.end_execution(status='failed')
            return False
    
    def run_pipeline(self) -> None:
        """Execute the complete pipeline"""
        logger.info("")
        logger.info("=" * 70)
        logger.info("INICIANDO PIPELINE COMPLETA DE ENGENHARIA DE DADOS")
        logger.info("=" * 70)
        logger.info("")
        logger.info("Arquitetura:")
        logger.info("  ERP (PostgreSQL)")
        logger.info("  ↓ Extract")
        logger.info("  Raw Layer (Parquet)")
        logger.info("  ↓ Curated")
        logger.info("  Curated Layer (Dimensional Model - Parquet)")
        logger.info("  ↓ Load DW")
        logger.info("  DW PostgreSQL (Schema dw)")
        logger.info("  ↓ Analytics")
        logger.info("  Analytics Layer (Business Metrics - Parquet)")
        logger.info("  ↓ Tests")
        logger.info("  Validação Completa")
        logger.info("")
        
        # Execute pipeline steps
        extract_success = self.run_extract()
        
        if extract_success:
            curated_success = self.run_curated()
            
            if curated_success:
                load_dw_success = self.run_load_dw()
                
                if load_dw_success:
                    analytics_success = self.run_analytics()
                    
                    if analytics_success:
                        tests_success = self.run_tests()
        
        # Print final summary
        self.print_summary()
    
    def print_summary(self) -> None:
        """Print pipeline execution summary"""
        logger.info("")
        logger.info("=" * 70)
        logger.info("RESUMO DA EXECUÇÃO DA PIPELINE")
        logger.info("=" * 70)
        logger.info("")
        
        logger.info(f"Passos Concluídos: {len(self.steps_completed)}")
        for step in self.steps_completed:
            logger.info(f"  ✓ {step}")
        
        if self.steps_failed:
            logger.info("")
            logger.info(f"Passos Falhados: {len(self.steps_failed)}")
            for step in self.steps_failed:
                logger.info(f"  ✗ {step}")
        
        logger.info("")
        logger.info("=" * 70)
        
        if not self.steps_failed:
            logger.info("✓ PIPELINE CONCLUÍDA COM SUCESSO!")
            logger.info("Todas as camadas foram processadas e validadas.")
        else:
            logger.warning(f"✗ {len(self.steps_failed)} passo(s) falhou(aram).")
            logger.warning("Verifique os erros acima para mais detalhes.")
        
        logger.info("=" * 70)
        logger.info("")


def main():
    """Main function"""
    orchestrator = PipelineOrchestrator()
    orchestrator.run_pipeline()


if __name__ == "__main__":
    main()
