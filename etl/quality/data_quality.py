"""
Data Quality Validation Framework
Validates business rules and data quality across all pipeline layers.

This module provides comprehensive data quality checks for:
- Raw Layer (extracted from ERP)
- Curated Layer (dimensional model)
- Analytics Layer (business metrics)
"""

import logging
from pathlib import Path
from typing import Dict, List, Tuple, Any
import pandas as pd

# Add parent directory to path to import config
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from config.settings import (
    RAW_DATA_DIR,
    CURATED_DATA_DIR,
    ANALYTICS_DATA_DIR,
    RAW_CLIENTES_FILE,
    RAW_PRODUTOS_FILE,
    RAW_PEDIDOS_FILE,
    RAW_ITENS_PEDIDO_FILE,
    CURATED_DIM_CLIENTE_FILE,
    CURATED_DIM_PRODUTO_FILE,
    CURATED_DIM_DATA_FILE,
    CURATED_FATO_VENDAS_FILE,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class DataQualityValidator:
    """Validates data quality across all pipeline layers"""
    
    def __init__(self):
        self.validation_results = []
        self.total_validations = 0
        self.passed_validations = 0
        self.failed_validations = 0
    
    def record_validation(self, validation_name: str, passed: bool, details: str = "") -> None:
        """Record validation result"""
        self.validation_results.append((validation_name, passed, details))
        self.total_validations += 1
        if passed:
            self.passed_validations += 1
            logger.info(f"✓ {validation_name}: {details}")
        else:
            self.failed_validations += 1
            logger.error(f"✗ {validation_name}: {details}")
    
    def validate_raw_layer(self) -> bool:
        """Validate Raw Layer data quality"""
        logger.info("")
        logger.info("=" * 70)
        logger.info("VALIDAÇÃO DE QUALIDADE - RAW LAYER")
        logger.info("=" * 70)
        logger.info("")
        
        all_passed = True
        
        # Validate clientes.parquet
        if RAW_CLIENTES_FILE.exists():
            df = pd.read_parquet(RAW_CLIENTES_FILE)
            
            # Check for null values in critical columns
            if df['id_cliente'].isnull().any():
                self.record_validation("Clientes - id_cliente não nulo", False, f"{df['id_cliente'].isnull().sum()} registros nulos")
                all_passed = False
            else:
                self.record_validation("Clientes - id_cliente não nulo", True, f"{len(df)} registros válidos")
            
            if df['nome'].isnull().any():
                self.record_validation("Clientes - nome não nulo", False, f"{df['nome'].isnull().sum()} registros nulos")
                all_passed = False
            else:
                self.record_validation("Clientes - nome não nulo", True, f"{len(df)} registros válidos")
            
            if df['cidade'].isnull().any():
                self.record_validation("Clientes - cidade não nulo", False, f"{df['cidade'].isnull().sum()} registros nulos")
                all_passed = False
            else:
                self.record_validation("Clientes - cidade não nulo", True, f"{len(df)} registros válidos")
        else:
            self.record_validation("Clientes - arquivo existe", False, "Arquivo não encontrado")
            all_passed = False
        
        # Validate produtos.parquet
        if RAW_PRODUTOS_FILE.exists():
            df = pd.read_parquet(RAW_PRODUTOS_FILE)
            
            # Check for null values in critical columns
            if df['id_produto'].isnull().any():
                self.record_validation("Produtos - id_produto não nulo", False, f"{df['id_produto'].isnull().sum()} registros nulos")
                all_passed = False
            else:
                self.record_validation("Produtos - id_produto não nulo", True, f"{len(df)} registros válidos")
            
            if df['nome'].isnull().any():
                self.record_validation("Produtos - nome não nulo", False, f"{df['nome'].isnull().sum()} registros nulos")
                all_passed = False
            else:
                self.record_validation("Produtos - nome não nulo", True, f"{len(df)} registros válidos")
            
            # Business rule: preço > 0
            if (df['preco'] <= 0).any():
                self.record_validation("Produtos - preço > 0", False, f"{(df['preco'] <= 0).sum()} registros com preço <= 0")
                all_passed = False
            else:
                self.record_validation("Produtos - preço > 0", True, f"{len(df)} registros válidos")
        else:
            self.record_validation("Produtos - arquivo existe", False, "Arquivo não encontrado")
            all_passed = False
        
        # Validate pedidos.parquet
        if RAW_PEDIDOS_FILE.exists():
            df = pd.read_parquet(RAW_PEDIDOS_FILE)
            
            # Check for null values in critical columns
            if df['id_pedido'].isnull().any():
                self.record_validation("Pedidos - id_pedido não nulo", False, f"{df['id_pedido'].isnull().sum()} registros nulos")
                all_passed = False
            else:
                self.record_validation("Pedidos - id_pedido não nulo", True, f"{len(df)} registros válidos")
            
            if df['id_cliente'].isnull().any():
                self.record_validation("Pedidos - id_cliente não nulo", False, f"{df['id_cliente'].isnull().sum()} registros nulos")
                all_passed = False
            else:
                self.record_validation("Pedidos - id_cliente não nulo", True, f"{len(df)} registros válidos")
            
            if df['data_pedido'].isnull().any():
                self.record_validation("Pedidos - data_pedido não nulo", False, f"{df['data_pedido'].isnull().sum()} registros nulos")
                all_passed = False
            else:
                self.record_validation("Pedidos - data_pedido não nulo", True, f"{len(df)} registros válidos")
        else:
            self.record_validation("Pedidos - arquivo existe", False, "Arquivo não encontrado")
            all_passed = False
        
        # Validate itens_pedido.parquet
        if RAW_ITENS_PEDIDO_FILE.exists():
            df = pd.read_parquet(RAW_ITENS_PEDIDO_FILE)
            
            # Check for null values in critical columns
            if df['id_item'].isnull().any():
                self.record_validation("Itens Pedido - id_item não nulo", False, f"{df['id_item'].isnull().sum()} registros nulos")
                all_passed = False
            else:
                self.record_validation("Itens Pedido - id_item não nulo", True, f"{len(df)} registros válidos")
            
            if df['id_pedido'].isnull().any():
                self.record_validation("Itens Pedido - id_pedido não nulo", False, f"{df['id_pedido'].isnull().sum()} registros nulos")
                all_passed = False
            else:
                self.record_validation("Itens Pedido - id_pedido não nulo", True, f"{len(df)} registros válidos")
            
            if df['id_produto'].isnull().any():
                self.record_validation("Itens Pedido - id_produto não nulo", False, f"{df['id_produto'].isnull().sum()} registros nulos")
                all_passed = False
            else:
                self.record_validation("Itens Pedido - id_produto não nulo", True, f"{len(df)} registros válidos")
            
            # Business rule: quantidade > 0
            if (df['quantidade'] <= 0).any():
                self.record_validation("Itens Pedido - quantidade > 0", False, f"{(df['quantidade'] <= 0).sum()} registros com quantidade <= 0")
                all_passed = False
            else:
                self.record_validation("Itens Pedido - quantidade > 0", True, f"{len(df)} registros válidos")
            
            # Business rule: preco_unitario > 0
            if (df['preco_unitario'] <= 0).any():
                self.record_validation("Itens Pedido - preco_unitario > 0", False, f"{(df['preco_unitario'] <= 0).sum()} registros com preco_unitario <= 0")
                all_passed = False
            else:
                self.record_validation("Itens Pedido - preco_unitario > 0", True, f"{len(df)} registros válidos")
        else:
            self.record_validation("Itens Pedido - arquivo existe", False, "Arquivo não encontrado")
            all_passed = False
        
        return all_passed
    
    def validate_curated_layer(self) -> bool:
        """Validate Curated Layer data quality"""
        logger.info("")
        logger.info("=" * 70)
        logger.info("VALIDAÇÃO DE QUALIDADE - CURATED LAYER")
        logger.info("=" * 70)
        logger.info("")
        
        all_passed = True
        
        # Validate dim_cliente.parquet
        if CURATED_DIM_CLIENTE_FILE.exists():
            df = pd.read_parquet(CURATED_DIM_CLIENTE_FILE)
            
            if df['id_cliente'].isnull().any():
                self.record_validation("Dim Cliente - id_cliente não nulo", False, f"{df['id_cliente'].isnull().sum()} registros nulos")
                all_passed = False
            else:
                self.record_validation("Dim Cliente - id_cliente não nulo", True, f"{len(df)} registros válidos")
            
            if df['nome'].isnull().any():
                self.record_validation("Dim Cliente - nome não nulo", False, f"{df['nome'].isnull().sum()} registros nulos")
                all_passed = False
            else:
                self.record_validation("Dim Cliente - nome não nulo", True, f"{len(df)} registros válidos")
            
            if df['cidade'].isnull().any():
                self.record_validation("Dim Cliente - cidade não nulo", False, f"{df['cidade'].isnull().sum()} registros nulos")
                all_passed = False
            else:
                self.record_validation("Dim Cliente - cidade não nulo", True, f"{len(df)} registros válidos")
        else:
            self.record_validation("Dim Cliente - arquivo existe", False, "Arquivo não encontrado")
            all_passed = False
        
        # Validate dim_produto.parquet
        if CURATED_DIM_PRODUTO_FILE.exists():
            df = pd.read_parquet(CURATED_DIM_PRODUTO_FILE)
            
            if df['id_produto'].isnull().any():
                self.record_validation("Dim Produto - id_produto não nulo", False, f"{df['id_produto'].isnull().sum()} registros nulos")
                all_passed = False
            else:
                self.record_validation("Dim Produto - id_produto não nulo", True, f"{len(df)} registros válidos")
            
            if df['nome'].isnull().any():
                self.record_validation("Dim Produto - nome não nulo", False, f"{df['nome'].isnull().sum()} registros nulos")
                all_passed = False
            else:
                self.record_validation("Dim Produto - nome não nulo", True, f"{len(df)} registros válidos")
            
            # Business rule: preco > 0
            if (df['preco'] <= 0).any():
                self.record_validation("Dim Produto - preco > 0", False, f"{(df['preco'] <= 0).sum()} registros com preco <= 0")
                all_passed = False
            else:
                self.record_validation("Dim Produto - preco > 0", True, f"{len(df)} registros válidos")
        else:
            self.record_validation("Dim Produto - arquivo existe", False, "Arquivo não encontrado")
            all_passed = False
        
        # Validate fato_vendas.parquet
        if CURATED_FATO_VENDAS_FILE.exists():
            df = pd.read_parquet(CURATED_FATO_VENDAS_FILE)
            
            if df['id_pedido'].isnull().any():
                self.record_validation("Fato Vendas - id_pedido não nulo", False, f"{df['id_pedido'].isnull().sum()} registros nulos")
                all_passed = False
            else:
                self.record_validation("Fato Vendas - id_pedido não nulo", True, f"{len(df)} registros válidos")
            
            if df['id_cliente'].isnull().any():
                self.record_validation("Fato Vendas - id_cliente não nulo", False, f"{df['id_cliente'].isnull().sum()} registros nulos")
                all_passed = False
            else:
                self.record_validation("Fato Vendas - id_cliente não nulo", True, f"{len(df)} registros válidos")
            
            if df['id_produto'].isnull().any():
                self.record_validation("Fato Vendas - id_produto não nulo", False, f"{df['id_produto'].isnull().sum()} registros nulos")
                all_passed = False
            else:
                self.record_validation("Fato Vendas - id_produto não nulo", True, f"{len(df)} registros válidos")
            
            # Business rule: quantidade > 0
            if (df['quantidade'] <= 0).any():
                self.record_validation("Fato Vendas - quantidade > 0", False, f"{(df['quantidade'] <= 0).sum()} registros com quantidade <= 0")
                all_passed = False
            else:
                self.record_validation("Fato Vendas - quantidade > 0", True, f"{len(df)} registros válidos")
            
            # Business rule: preco_unitario > 0
            if (df['preco_unitario'] <= 0).any():
                self.record_validation("Fato Vendas - preco_unitario > 0", False, f"{(df['preco_unitario'] <= 0).sum()} registros com preco_unitario <= 0")
                all_passed = False
            else:
                self.record_validation("Fato Vendas - preco_unitario > 0", True, f"{len(df)} registros válidos")
            
            # Business rule: valor_total > 0
            if (df['valor_total'] <= 0).any():
                self.record_validation("Fato Vendas - valor_total > 0", False, f"{(df['valor_total'] <= 0).sum()} registros com valor_total <= 0")
                all_passed = False
            else:
                self.record_validation("Fato Vendas - valor_total > 0", True, f"{len(df)} registros válidos")
        else:
            self.record_validation("Fato Vendas - arquivo existe", False, "Arquivo não encontrado")
            all_passed = False
        
        return all_passed
    
    def validate_business_rules(self) -> bool:
        """Validate cross-layer business rules"""
        logger.info("")
        logger.info("=" * 70)
        logger.info("VALIDAÇÃO DE REGRAS DE NEGÓCIO")
        logger.info("=" * 70)
        logger.info("")
        
        all_passed = True
        
        # Business rule: Every pedido must have at least one item
        if RAW_PEDIDOS_FILE.exists() and RAW_ITENS_PEDIDO_FILE.exists():
            pedidos_df = pd.read_parquet(RAW_PEDIDOS_FILE)
            itens_df = pd.read_parquet(RAW_ITENS_PEDIDO_FILE)
            
            pedidos_com_itens = itens_df['id_pedido'].nunique()
            total_pedidos = pedidos_df['id_pedido'].nunique()
            
            if pedidos_com_itens == total_pedidos:
                self.record_validation("Pedidos - todos têm itens", True, f"{total_pedidos} pedidos com itens")
            else:
                pedidos_sem_itens = total_pedidos - pedidos_com_itens
                self.record_validation("Pedidos - todos têm itens", False, f"{pedidos_sem_itens} pedidos sem itens")
                all_passed = False
        else:
            self.record_validation("Pedidos - todos têm itens", False, "Arquivos não encontrados")
            all_passed = False
        
        # Business rule: All clientes in pedidos must exist in clientes
        if RAW_PEDIDOS_FILE.exists() and RAW_CLIENTES_FILE.exists():
            pedidos_df = pd.read_parquet(RAW_PEDIDOS_FILE)
            clientes_df = pd.read_parquet(RAW_CLIENTES_FILE)
            
            clientes_em_pedidos = set(pedidos_df['id_cliente'].unique())
            clientes_existentes = set(clientes_df['id_cliente'].unique())
            
            clientes_orfaos = clientes_em_pedidos - clientes_existentes
            
            if len(clientes_orfaos) == 0:
                self.record_validation("Pedidos - clientes válidos", True, f"{len(clientes_em_pedidos)} clientes válidos")
            else:
                self.record_validation("Pedidos - clientes válidos", False, f"{len(clientes_orfaos)} clientes órfãos")
                all_passed = False
        else:
            self.record_validation("Pedidos - clientes válidos", False, "Arquivos não encontrados")
            all_passed = False
        
        # Business rule: All produtos in itens_pedido must exist in produtos
        if RAW_ITENS_PEDIDO_FILE.exists() and RAW_PRODUTOS_FILE.exists():
            itens_df = pd.read_parquet(RAW_ITENS_PEDIDO_FILE)
            produtos_df = pd.read_parquet(RAW_PRODUTOS_FILE)
            
            produtos_em_itens = set(itens_df['id_produto'].unique())
            produtos_existentes = set(produtos_df['id_produto'].unique())
            
            produtos_orfaos = produtos_em_itens - produtos_existentes
            
            if len(produtos_orfaos) == 0:
                self.record_validation("Itens Pedido - produtos válidos", True, f"{len(produtos_em_itens)} produtos válidos")
            else:
                self.record_validation("Itens Pedido - produtos válidos", False, f"{len(produtos_orfaos)} produtos órfãos")
                all_passed = False
        else:
            self.record_validation("Itens Pedido - produtos válidos", False, "Arquivos não encontrados")
            all_passed = False
        
        return all_passed
    
    def print_summary(self) -> None:
        """Print validation summary"""
        logger.info("")
        logger.info("=" * 70)
        logger.info("RESUMO DA VALIDAÇÃO DE QUALIDADE")
        logger.info("=" * 70)
        logger.info(f"Total de Validações: {self.total_validations}")
        logger.info(f"Validações Aprovadas: {self.passed_validations}")
        logger.info(f"Validações Falhadas: {self.failed_validations}")
        logger.info(f"Taxa de Sucesso: {(self.passed_validations/self.total_validations*100):.1f}%")
        logger.info("")
        
        if self.failed_validations > 0:
            logger.info("Validações Falhadas:")
            for validation_name, passed, details in self.validation_results:
                if not passed:
                    logger.info(f"  ✗ {validation_name}: {details}")
            logger.info("")
        
        logger.info("=" * 70)
        
        if self.failed_validations == 0:
            logger.info("✓ TODAS AS VALIDAÇÕES PASSARAM! Dados com qualidade garantida.")
        else:
            logger.warning(f"✗ {self.failed_validations} validação(ões) falhou(aram). Verifique os erros acima.")
    
    def run_all_validations(self) -> bool:
        """Run all data quality validations"""
        logger.info("")
        logger.info("=" * 70)
        logger.info("INICIANDO VALIDAÇÃO DE QUALIDADE DE DADOS")
        logger.info("=" * 70)
        logger.info("")
        
        try:
            # Run validations
            raw_passed = self.validate_raw_layer()
            curated_passed = self.validate_curated_layer()
            business_passed = self.validate_business_rules()
            
            # Print summary
            self.print_summary()
            
            return raw_passed and curated_passed and business_passed
            
        except Exception as e:
            logger.error(f"Erro fatal durante validação de qualidade: {e}")
            return False


def main():
    """Main function"""
    validator = DataQualityValidator()
    success = validator.run_all_validations()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
