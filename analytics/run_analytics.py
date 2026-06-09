"""
Analytics Orchestration Script
Executes all analytics metrics and generates a final report.

This script orchestrates the execution of all analytics metrics:
- Receita Total
- Receita por Cliente
- Receita por Produto
- Receita por Cidade
- Ticket Médio
- Produto Mais Vendido
- Top 5 Clientes
- Top 5 Produtos
- Receita Mensal

All metrics are calculated exclusively from the Curated Layer using DuckDB.
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple
import logging

import pandas as pd

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent))

from config.settings import ANALYTICS_DATA_DIR

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class AnalyticsOrchestrator:
    """Orchestrates the execution of all analytics metrics"""
    
    def __init__(self):
        self.results: Dict[str, Tuple[int, pd.DataFrame]] = {}
        self.analytics_dir = ANALYTICS_DATA_DIR
    
    def execute_receita_total(self) -> pd.DataFrame:
        """Execute receita_total analytics"""
        logger.info("[INFO] Receita Total calculada")
        from analytics.receita_total import calculate_total_revenue
        df = calculate_total_revenue()
        self.results['receita_total'] = (len(df), df)
        return df
    
    def execute_receita_por_cliente(self) -> pd.DataFrame:
        """Execute receita_por_cliente analytics"""
        logger.info("[INFO] Receita por Cliente calculada")
        from analytics.receita_por_cliente import calculate_revenue_by_client
        df = calculate_revenue_by_client()
        self.results['receita_por_cliente'] = (len(df), df)
        return df
    
    def execute_receita_por_produto(self) -> pd.DataFrame:
        """Execute receita_por_produto analytics"""
        logger.info("[INFO] Receita por Produto calculada")
        from analytics.receita_por_produto import calculate_revenue_by_product
        df = calculate_revenue_by_product()
        self.results['receita_por_produto'] = (len(df), df)
        return df
    
    def execute_receita_por_cidade(self) -> pd.DataFrame:
        """Execute receita_por_cidade analytics"""
        logger.info("[INFO] Receita por Cidade calculada")
        from analytics.receita_por_cidade import calculate_revenue_by_city
        df = calculate_revenue_by_city()
        self.results['receita_por_cidade'] = (len(df), df)
        return df
    
    def execute_ticket_medio(self) -> pd.DataFrame:
        """Execute ticket_medio analytics"""
        logger.info("[INFO] Ticket Médio calculado")
        from analytics.ticket_medio import calculate_average_ticket
        df = calculate_average_ticket()
        self.results['ticket_medio'] = (len(df), df)
        return df
    
    def execute_produto_mais_vendido(self) -> pd.DataFrame:
        """Execute produto_mais_vendido analytics"""
        logger.info("[INFO] Produto Mais Vendido calculado")
        from analytics.produto_mais_vendido import calculate_most_sold_product
        df = calculate_most_sold_product()
        self.results['produto_mais_vendido'] = (len(df), df)
        return df
    
    def execute_top_clientes(self) -> pd.DataFrame:
        """Execute top_clientes analytics"""
        logger.info("[INFO] Top Clientes calculado")
        from analytics.top_clientes import calculate_top_clients
        df = calculate_top_clients()
        self.results['top_clientes'] = (len(df), df)
        return df
    
    def execute_top_produtos(self) -> pd.DataFrame:
        """Execute top_produtos analytics"""
        logger.info("[INFO] Top Produtos calculado")
        from analytics.top_produtos import calculate_top_produtos
        df = calculate_top_produtos()
        self.results['top_produtos'] = (len(df), df)
        return df
    
    def execute_receita_mensal(self) -> pd.DataFrame:
        """Execute receita_mensal analytics"""
        logger.info("[INFO] Receita Mensal calculada")
        from analytics.receita_mensal import calculate_receita_mensal
        df = calculate_receita_mensal()
        self.results['receita_mensal'] = (len(df), df)
        return df
    
    def run_all_analytics(self) -> None:
        """Execute all analytics metrics"""
        logger.info("")
        logger.info("=" * 60)
        logger.info("INICIANDO ANALYTICS LAYER")
        logger.info("=" * 60)
        logger.info("")
        
        try:
            # Execute all metrics
            self.execute_receita_total()
            self.execute_receita_por_cliente()
            self.execute_receita_por_produto()
            self.execute_receita_por_cidade()
            self.execute_ticket_medio()
            self.execute_produto_mais_vendido()
            self.execute_top_clientes()
            self.execute_top_produtos()
            self.execute_receita_mensal()
            
            # Print final report
            self.print_final_report()
            
            logger.info("")
            logger.info("[INFO] Analytics concluído")
            logger.info("")
            
        except Exception as e:
            logger.error(f"Erro durante execução das analytics: {e}")
            raise
    
    def print_final_report(self) -> None:
        """Print final report with all metrics"""
        logger.info("")
        logger.info("=" * 60)
        logger.info("RELATÓRIO FINAL - ANALYTICS LAYER")
        logger.info("=" * 60)
        logger.info("")
        
        # Print table header
        logger.info(f"{'Métrica':<25} {'Registros':<10}")
        logger.info("-" * 35)
        
        # Print each metric
        metric_names = {
            'receita_total': 'receita_total',
            'receita_por_cliente': 'receita_por_cliente',
            'receita_por_produto': 'receita_por_produto',
            'receita_por_cidade': 'receita_por_cidade',
            'ticket_medio': 'ticket_medio',
            'produto_mais_vendido': 'produto_mais_vendido',
            'top_clientes': 'top_clientes',
            'top_produtos': 'top_produtos',
            'receita_mensal': 'receita_mensal'
        }
        
        for key, name in metric_names.items():
            if key in self.results:
                count, _ = self.results[key]
                logger.info(f"{name:<25} {count:<10}")
        
        logger.info("")
        logger.info("=" * 60)
        logger.info(f"Total de métricas geradas: {len(self.results)}")
        logger.info(f"Arquivos salvos em: {self.analytics_dir}")
        logger.info("=" * 60)


def main():
    """Main function"""
    orchestrator = AnalyticsOrchestrator()
    orchestrator.run_all_analytics()


if __name__ == "__main__":
    main()
