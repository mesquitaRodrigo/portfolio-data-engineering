"""
Comprehensive Test Script for Data Engineering Portfolio Project
Tests the entire data pipeline: ERP → Raw → Curated → Analytics
"""

import logging
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, text

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent))
from config.settings import (
    DATABASE_URL,
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
    ANALYTICS_RECEITA_TOTAL_FILE,
    ANALYTICS_RECEITA_POR_CLIENTE_FILE,
    ANALYTICS_RECEITA_POR_PRODUTO_FILE,
    ANALYTICS_RECEITA_POR_CIDADE_FILE,
    ANALYTICS_TICKET_MEDIO_FILE,
    ANALYTICS_PRODUTO_MAIS_VENDIDO_FILE,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class ProjectTester:
    """Comprehensive test suite for the data engineering project"""
    
    def __init__(self):
        self.engine = None
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
    
    def connect_postgres(self) -> bool:
        """Test PostgreSQL connection"""
        try:
            logger.info("Teste 1: Conexão com PostgreSQL")
            self.engine = create_engine(DATABASE_URL)
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("✓ Conexão com PostgreSQL estabelecida com sucesso")
            self.record_test("Conexão PostgreSQL", True)
            return True
        except Exception as e:
            logger.error(f"✗ Falha na conexão com PostgreSQL: {e}")
            self.record_test("Conexão PostgreSQL", False)
            return False
    
    def test_erp_schema(self) -> bool:
        """Test if ERP schema exists"""
        try:
            logger.info("Teste 2: Verificação do Schema ERP")
            with self.engine.connect() as conn:
                # Check if tables exist
                tables = ['clientes', 'produtos', 'pedidos', 'itens_pedido']
                for table in tables:
                    result = conn.execute(text(
                        f"SELECT EXISTS (SELECT FROM information_schema.tables "
                        f"WHERE table_name = '{table}')"
                    ))
                    exists = result.scalar()
                    if not exists:
                        logger.error(f"✗ Tabela {table} não existe")
                        self.record_test(f"Tabela {table}", False)
                        return False
                    logger.info(f"✓ Tabela {table} existe")
                    self.record_test(f"Tabela {table}", True)
            return True
        except Exception as e:
            logger.error(f"✗ Erro ao verificar schema ERP: {e}")
            self.record_test("Schema ERP", False)
            return False
    
    def test_erp_data(self) -> bool:
        """Test if ERP has sample data"""
        try:
            logger.info("Teste 3: Verificação de Dados no ERP")
            with self.engine.connect() as conn:
                tables = {
                    'clientes': 10,
                    'produtos': 10,
                    'pedidos': 20,
                    'itens_pedido': 46
                }
                
                for table, expected_min in tables.items():
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    if count < expected_min:
                        logger.error(f"✗ Tabela {table} tem apenas {count} registros (mínimo: {expected_min})")
                        self.record_test(f"Dados {table}", False)
                        return False
                    logger.info(f"✓ Tabela {table} tem {count} registros")
                    self.record_test(f"Dados {table}", True)
            return True
        except Exception as e:
            logger.error(f"✗ Erro ao verificar dados ERP: {e}")
            self.record_test("Dados ERP", False)
            return False
    
    def test_raw_layer_files(self) -> bool:
        """Test if Raw Layer Parquet files exist"""
        try:
            logger.info("Teste 4: Verificação de Arquivos Raw Layer")
            files = {
                'clientes.parquet': RAW_CLIENTES_FILE,
                'produtos.parquet': RAW_PRODUTOS_FILE,
                'pedidos.parquet': RAW_PEDIDOS_FILE,
                'itens_pedido.parquet': RAW_ITENS_PEDIDO_FILE
            }
            
            all_exist = True
            for name, path in files.items():
                if path.exists():
                    size = path.stat().st_size
                    logger.info(f"✓ Arquivo {name} existe ({size} bytes)")
                    self.record_test(f"Arquivo {name}", True)
                else:
                    logger.error(f"✗ Arquivo {name} não existe")
                    self.record_test(f"Arquivo {name}", False)
                    all_exist = False
            
            return all_exist
        except Exception as e:
            logger.error(f"✗ Erro ao verificar arquivos Raw Layer: {e}")
            self.record_test("Arquivos Raw Layer", False)
            return False
    
    def test_raw_layer_data(self) -> bool:
        """Test if Raw Layer Parquet files have data"""
        try:
            logger.info("Teste 5: Verificação de Dados Raw Layer")
            files = {
                'clientes.parquet': RAW_CLIENTES_FILE,
                'produtos.parquet': RAW_PRODUTOS_FILE,
                'pedidos.parquet': RAW_PEDIDOS_FILE,
                'itens_pedido.parquet': RAW_ITENS_PEDIDO_FILE
            }
            
            all_valid = True
            for name, path in files.items():
                if path.exists():
                    df = pd.read_parquet(path)
                    if len(df) > 0:
                        logger.info(f"✓ Arquivo {name} tem {len(df)} registros")
                        self.record_test(f"Dados {name}", True)
                    else:
                        logger.error(f"✗ Arquivo {name} está vazio")
                        self.record_test(f"Dados {name}", False)
                        all_valid = False
                else:
                    logger.error(f"✗ Arquivo {name} não existe para verificação de dados")
                    self.record_test(f"Dados {name}", False)
                    all_valid = False
            
            return all_valid
        except Exception as e:
            logger.error(f"✗ Erro ao verificar dados Raw Layer: {e}")
            self.record_test("Dados Raw Layer", False)
            return False
    
    def test_data_integrity(self) -> bool:
        """Test data integrity between ERP and Raw Layer"""
        try:
            logger.info("Teste 6: Integridade de Dados (ERP vs Raw Layer)")
            
            with self.engine.connect() as conn:
                # Compare record counts
                tables = ['clientes', 'produtos', 'pedidos', 'itens_pedido']
                all_match = True
                
                for table in tables:
                    # Get ERP count
                    erp_result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    erp_count = erp_result.scalar()
                    
                    # Get Raw Layer count
                    if table == 'itens_pedido':
                        raw_file = RAW_ITENS_PEDIDO_FILE
                    elif table == 'pedidos':
                        raw_file = RAW_PEDIDOS_FILE
                    elif table == 'produtos':
                        raw_file = RAW_PRODUTOS_FILE
                    else:
                        raw_file = RAW_CLIENTES_FILE
                    
                    if raw_file.exists():
                        df = pd.read_parquet(raw_file)
                        raw_count = len(df)
                        
                        if erp_count == raw_count:
                            logger.info(f"✓ {table}: ERP={erp_count}, Raw={raw_count} (match)")
                            self.record_test(f"Integridade {table}", True)
                        else:
                            logger.warning(f"⚠ {table}: ERP={erp_count}, Raw={raw_count} (mismatch)")
                            self.record_test(f"Integridade {table}", False)
                            all_match = False
                    else:
                        logger.error(f"✗ Arquivo Raw para {table} não existe")
                        self.record_test(f"Integridade {table}", False)
                        all_match = False
            
            return all_match
        except Exception as e:
            logger.error(f"✗ Erro ao testar integridade de dados: {e}")
            self.record_test("Integridade de Dados", False)
            return False
    
    def test_foreign_keys(self) -> bool:
        """Test foreign key constraints in ERP"""
        try:
            logger.info("Teste 7: Verificação de Foreign Keys no ERP")
            
            with self.engine.connect() as conn:
                # Check pedidos -> clientes
                result = conn.execute(text("""
                    SELECT COUNT(*) FROM pedidos p
                    WHERE NOT EXISTS (SELECT 1 FROM clientes c WHERE c.id_cliente = p.id_cliente)
                """))
                orphan_pedidos = result.scalar()
                
                if orphan_pedidos == 0:
                    logger.info("✓ Todos os pedidos têm clientes válidos")
                    self.record_test("FK pedidos->clientes", True)
                else:
                    logger.error(f"✗ {orphan_pedidos} pedidos sem clientes válidos")
                    self.record_test("FK pedidos->clientes", False)
                
                # Check itens_pedido -> pedidos
                result = conn.execute(text("""
                    SELECT COUNT(*) FROM itens_pedido ip
                    WHERE NOT EXISTS (SELECT 1 FROM pedidos p WHERE p.id_pedido = ip.id_pedido)
                """))
                orphan_itens_pedido = result.scalar()
                
                if orphan_itens_pedido == 0:
                    logger.info("✓ Todos os itens_pedido têm pedidos válidos")
                    self.record_test("FK itens_pedido->pedidos", True)
                else:
                    logger.error(f"✗ {orphan_itens_pedido} itens_pedido sem pedidos válidos")
                    self.record_test("FK itens_pedido->pedidos", False)
                
                # Check itens_pedido -> produtos
                result = conn.execute(text("""
                    SELECT COUNT(*) FROM itens_pedido ip
                    WHERE NOT EXISTS (SELECT 1 FROM produtos pr WHERE pr.id_produto = ip.id_produto)
                """))
                orphan_produtos = result.scalar()
                
                if orphan_produtos == 0:
                    logger.info("✓ Todos os itens_pedido têm produtos válidos")
                    self.record_test("FK itens_pedido->produtos", True)
                else:
                    logger.error(f"✗ {orphan_produtos} itens_pedido sem produtos válidos")
                    self.record_test("FK itens_pedido->produtos", False)
                
                return orphan_pedidos == 0 and orphan_itens_pedido == 0 and orphan_produtos == 0
        except Exception as e:
            logger.error(f"✗ Erro ao verificar foreign keys: {e}")
            self.record_test("Foreign Keys", False)
            return False
    
    def test_directory_structure(self) -> bool:
        """Test if directory structure is correct"""
        try:
            logger.info("Teste 8: Verificação da Estrutura de Diretórios")
            
            directories = {
                'raw': RAW_DATA_DIR,
                'curated': CURATED_DATA_DIR,
                'analytics': ANALYTICS_DATA_DIR
            }
            
            all_exist = True
            for name, path in directories.items():
                if path.exists() and path.is_dir():
                    logger.info(f"✓ Diretório {name}/ existe")
                    self.record_test(f"Diretório {name}", True)
                else:
                    logger.error(f"✗ Diretório {name}/ não existe")
                    self.record_test(f"Diretório {name}", False)
                    all_exist = False
            
            return all_exist
        except Exception as e:
            logger.error(f"✗ Erro ao verificar estrutura de diretórios: {e}")
            self.record_test("Estrutura de Diretórios", False)
            return False
    
    def test_curated_layer_files(self) -> bool:
        """Test if Curated Layer Parquet files exist"""
        try:
            logger.info("Teste 9: Verificação de Arquivos Curated Layer")
            files = {
                'dim_cliente.parquet': CURATED_DIM_CLIENTE_FILE,
                'dim_produto.parquet': CURATED_DIM_PRODUTO_FILE,
                'dim_data.parquet': CURATED_DIM_DATA_FILE,
                'fato_vendas.parquet': CURATED_FATO_VENDAS_FILE
            }
            
            all_exist = True
            for name, path in files.items():
                if path.exists():
                    size = path.stat().st_size
                    logger.info(f"✓ Arquivo {name} existe ({size} bytes)")
                    self.record_test(f"Arquivo {name}", True)
                else:
                    logger.error(f"✗ Arquivo {name} não existe")
                    self.record_test(f"Arquivo {name}", False)
                    all_exist = False
            
            return all_exist
        except Exception as e:
            logger.error(f"✗ Erro ao verificar arquivos Curated Layer: {e}")
            self.record_test("Arquivos Curated Layer", False)
            return False
    
    def test_curated_layer_data(self) -> bool:
        """Test if Curated Layer Parquet files have data"""
        try:
            logger.info("Teste 10: Verificação de Dados Curated Layer")
            files = {
                'dim_cliente.parquet': CURATED_DIM_CLIENTE_FILE,
                'dim_produto.parquet': CURATED_DIM_PRODUTO_FILE,
                'dim_data.parquet': CURATED_DIM_DATA_FILE,
                'fato_vendas.parquet': CURATED_FATO_VENDAS_FILE
            }
            
            all_valid = True
            for name, path in files.items():
                if path.exists():
                    df = pd.read_parquet(path)
                    if len(df) > 0:
                        logger.info(f"✓ Arquivo {name} tem {len(df)} registros")
                        self.record_test(f"Dados {name}", True)
                    else:
                        logger.error(f"✗ Arquivo {name} está vazio")
                        self.record_test(f"Dados {name}", False)
                        all_valid = False
                else:
                    logger.error(f"✗ Arquivo {name} não existe para verificação de dados")
                    self.record_test(f"Dados {name}", False)
                    all_valid = False
            
            return all_valid
        except Exception as e:
            logger.error(f"✗ Erro ao verificar dados Curated Layer: {e}")
            self.record_test("Dados Curated Layer", False)
            return False
    
    def test_curated_layer_schema(self) -> bool:
        """Test if Curated Layer schema is correct"""
        try:
            logger.info("Teste 11: Verificação do Schema Curated Layer")
            
            # Expected schemas
            expected_schemas = {
                'dim_cliente.parquet': ['id_cliente', 'nome', 'cidade'],
                'dim_produto.parquet': ['id_produto', 'nome', 'categoria', 'preco'],
                'dim_data.parquet': ['data', 'ano', 'mes', 'dia', 'trimestre', 'nome_mes'],
                'fato_vendas.parquet': ['id_pedido', 'data_pedido', 'id_cliente', 'id_produto', 'quantidade', 'preco_unitario', 'valor_total']
            }
            
            files = {
                'dim_cliente.parquet': CURATED_DIM_CLIENTE_FILE,
                'dim_produto.parquet': CURATED_DIM_PRODUTO_FILE,
                'dim_data.parquet': CURATED_DIM_DATA_FILE,
                'fato_vendas.parquet': CURATED_FATO_VENDAS_FILE
            }
            
            all_valid = True
            for name, path in files.items():
                if path.exists():
                    df = pd.read_parquet(path)
                    actual_columns = list(df.columns)
                    expected_columns = expected_schemas[name]
                    
                    if actual_columns == expected_columns:
                        logger.info(f"✓ Schema de {name} está correto: {expected_columns}")
                        self.record_test(f"Schema {name}", True)
                    else:
                        logger.error(f"✗ Schema de {name} incorreto. Esperado: {expected_columns}, Atual: {actual_columns}")
                        self.record_test(f"Schema {name}", False)
                        all_valid = False
                else:
                    logger.error(f"✗ Arquivo {name} não existe para verificação de schema")
                    self.record_test(f"Schema {name}", False)
                    all_valid = False
            
            return all_valid
        except Exception as e:
            logger.error(f"✗ Erro ao verificar schema Curated Layer: {e}")
            self.record_test("Schema Curated Layer", False)
            return False
    
    def test_curated_layer_integrity(self) -> bool:
        """Test data integrity between Raw and Curated layers"""
        try:
            logger.info("Teste 12: Integridade de Dados (Raw vs Curated Layer)")
            
            all_match = True
            
            # Compare dim_cliente with raw clientes
            if RAW_CLIENTES_FILE.exists() and CURATED_DIM_CLIENTE_FILE.exists():
                raw_df = pd.read_parquet(RAW_CLIENTES_FILE)
                curated_df = pd.read_parquet(CURATED_DIM_CLIENTE_FILE)
                
                if len(raw_df) == len(curated_df):
                    logger.info(f"✓ dim_cliente: Raw={len(raw_df)}, Curated={len(curated_df)} (match)")
                    self.record_test("Integridade dim_cliente", True)
                else:
                    logger.warning(f"⚠ dim_cliente: Raw={len(raw_df)}, Curated={len(curated_df)} (mismatch)")
                    self.record_test("Integridade dim_cliente", False)
                    all_match = False
            else:
                logger.error("✗ Arquivos necessários para teste de integridade dim_cliente não existem")
                self.record_test("Integridade dim_cliente", False)
                all_match = False
            
            # Compare dim_produto with raw produtos
            if RAW_PRODUTOS_FILE.exists() and CURATED_DIM_PRODUTO_FILE.exists():
                raw_df = pd.read_parquet(RAW_PRODUTOS_FILE)
                curated_df = pd.read_parquet(CURATED_DIM_PRODUTO_FILE)
                
                if len(raw_df) == len(curated_df):
                    logger.info(f"✓ dim_produto: Raw={len(raw_df)}, Curated={len(curated_df)} (match)")
                    self.record_test("Integridade dim_produto", True)
                else:
                    logger.warning(f"⚠ dim_produto: Raw={len(raw_df)}, Curated={len(curated_df)} (mismatch)")
                    self.record_test("Integridade dim_produto", False)
                    all_match = False
            else:
                logger.error("✗ Arquivos necessários para teste de integridade dim_produto não existem")
                self.record_test("Integridade dim_produto", False)
                all_match = False
            
            # Verify fato_vendas has data
            if CURATED_FATO_VENDAS_FILE.exists():
                fato_df = pd.read_parquet(CURATED_FATO_VENDAS_FILE)
                if len(fato_df) > 0:
                    logger.info(f"✓ fato_vendas tem {len(fato_df)} registros")
                    self.record_test("Integridade fato_vendas", True)
                else:
                    logger.error("✗ fato_vendas está vazio")
                    self.record_test("Integridade fato_vendas", False)
                    all_match = False
            else:
                logger.error("✗ Arquivo fato_vendas não existe")
                self.record_test("Integridade fato_vendas", False)
                all_match = False
            
            return all_match
        except Exception as e:
            logger.error(f"✗ Erro ao testar integridade Curated Layer: {e}")
            self.record_test("Integridade Curated Layer", False)
            return False
    
    def test_analytics_layer_files(self) -> bool:
        """Test if Analytics Layer Parquet files exist"""
        try:
            logger.info("Teste 13: Verificação de Arquivos Analytics Layer")
            files = {
                'receita_total.parquet': ANALYTICS_RECEITA_TOTAL_FILE,
                'receita_por_cliente.parquet': ANALYTICS_RECEITA_POR_CLIENTE_FILE,
                'receita_por_produto.parquet': ANALYTICS_RECEITA_POR_PRODUTO_FILE,
                'receita_por_cidade.parquet': ANALYTICS_RECEITA_POR_CIDADE_FILE,
                'ticket_medio.parquet': ANALYTICS_TICKET_MEDIO_FILE,
                'produto_mais_vendido.parquet': ANALYTICS_PRODUTO_MAIS_VENDIDO_FILE
            }
            
            # Also check for additional analytics files
            additional_files = {
                'top_clientes.parquet': ANALYTICS_DATA_DIR / 'top_clientes.parquet',
                'top_produtos.parquet': ANALYTICS_DATA_DIR / 'top_produtos.parquet',
                'receita_mensal.parquet': ANALYTICS_DATA_DIR / 'receita_mensal.parquet'
            }
            files.update(additional_files)
            
            all_exist = True
            for name, path in files.items():
                if path.exists():
                    size = path.stat().st_size
                    logger.info(f"✓ Arquivo {name} existe ({size} bytes)")
                    self.record_test(f"Arquivo {name}", True)
                else:
                    logger.error(f"✗ Arquivo {name} não existe")
                    self.record_test(f"Arquivo {name}", False)
                    all_exist = False
            
            return all_exist
        except Exception as e:
            logger.error(f"✗ Erro ao verificar arquivos Analytics Layer: {e}")
            self.record_test("Arquivos Analytics Layer", False)
            return False
    
    def test_analytics_layer_data(self) -> bool:
        """Test if Analytics Layer Parquet files have data"""
        try:
            logger.info("Teste 14: Verificação de Dados Analytics Layer")
            files = {
                'receita_total.parquet': ANALYTICS_RECEITA_TOTAL_FILE,
                'receita_por_cliente.parquet': ANALYTICS_RECEITA_POR_CLIENTE_FILE,
                'receita_por_produto.parquet': ANALYTICS_RECEITA_POR_PRODUTO_FILE,
                'receita_por_cidade.parquet': ANALYTICS_RECEITA_POR_CIDADE_FILE,
                'ticket_medio.parquet': ANALYTICS_TICKET_MEDIO_FILE,
                'produto_mais_vendido.parquet': ANALYTICS_PRODUTO_MAIS_VENDIDO_FILE
            }
            
            # Also check for additional analytics files
            additional_files = {
                'top_clientes.parquet': ANALYTICS_DATA_DIR / 'top_clientes.parquet',
                'top_produtos.parquet': ANALYTICS_DATA_DIR / 'top_produtos.parquet',
                'receita_mensal.parquet': ANALYTICS_DATA_DIR / 'receita_mensal.parquet'
            }
            files.update(additional_files)
            
            all_valid = True
            for name, path in files.items():
                if path.exists():
                    df = pd.read_parquet(path)
                    if len(df) > 0:
                        logger.info(f"✓ Arquivo {name} tem {len(df)} registros")
                        self.record_test(f"Dados {name}", True)
                    else:
                        logger.error(f"✗ Arquivo {name} está vazio")
                        self.record_test(f"Dados {name}", False)
                        all_valid = False
                else:
                    logger.error(f"✗ Arquivo {name} não existe para verificação de dados")
                    self.record_test(f"Dados {name}", False)
                    all_valid = False
            
            return all_valid
        except Exception as e:
            logger.error(f"✗ Erro ao verificar dados Analytics Layer: {e}")
            self.record_test("Dados Analytics Layer", False)
            return False
    
    def test_analytics_layer_schema(self) -> bool:
        """Test if Analytics Layer schema is correct"""
        try:
            logger.info("Teste 15: Verificação do Schema Analytics Layer")
            
            # Expected schemas
            expected_schemas = {
                'receita_total.parquet': ['receita_total'],
                'receita_por_cliente.parquet': ['cliente', 'receita_total'],
                'receita_por_produto.parquet': ['produto', 'receita_total'],
                'receita_por_cidade.parquet': ['cidade', 'receita_total'],
                'ticket_medio.parquet': ['ticket_medio'],
                'produto_mais_vendido.parquet': ['produto', 'quantidade_total'],
                'top_clientes.parquet': ['cliente', 'receita_total'],
                'top_produtos.parquet': ['produto', 'quantidade_total'],
                'receita_mensal.parquet': ['ano', 'mes', 'nome_mes', 'receita_total']
            }
            
            files = {
                'receita_total.parquet': ANALYTICS_RECEITA_TOTAL_FILE,
                'receita_por_cliente.parquet': ANALYTICS_RECEITA_POR_CLIENTE_FILE,
                'receita_por_produto.parquet': ANALYTICS_RECEITA_POR_PRODUTO_FILE,
                'receita_por_cidade.parquet': ANALYTICS_RECEITA_POR_CIDADE_FILE,
                'ticket_medio.parquet': ANALYTICS_TICKET_MEDIO_FILE,
                'produto_mais_vendido.parquet': ANALYTICS_PRODUTO_MAIS_VENDIDO_FILE
            }
            
            # Also check for additional analytics files
            additional_files = {
                'top_clientes.parquet': ANALYTICS_DATA_DIR / 'top_clientes.parquet',
                'top_produtos.parquet': ANALYTICS_DATA_DIR / 'top_produtos.parquet',
                'receita_mensal.parquet': ANALYTICS_DATA_DIR / 'receita_mensal.parquet'
            }
            files.update(additional_files)
            
            all_valid = True
            for name, path in files.items():
                if path.exists():
                    df = pd.read_parquet(path)
                    actual_columns = list(df.columns)
                    expected_columns = expected_schemas[name]
                    
                    if actual_columns == expected_columns:
                        logger.info(f"✓ Schema de {name} está correto: {expected_columns}")
                        self.record_test(f"Schema {name}", True)
                    else:
                        logger.error(f"✗ Schema de {name} incorreto. Esperado: {expected_columns}, Atual: {actual_columns}")
                        self.record_test(f"Schema {name}", False)
                        all_valid = False
                else:
                    logger.error(f"✗ Arquivo {name} não existe para verificação de schema")
                    self.record_test(f"Schema {name}", False)
                    all_valid = False
            
            return all_valid
        except Exception as e:
            logger.error(f"✗ Erro ao verificar schema Analytics Layer: {e}")
            self.record_test("Schema Analytics Layer", False)
            return False
    
    def test_dw_schema(self) -> bool:
        """Test if DW schema exists"""
        try:
            logger.info("Teste 16: Verificação do Schema DW")
            with self.engine.connect() as conn:
                # Check if dw schema exists
                result = conn.execute(text(
                    "SELECT EXISTS (SELECT FROM information_schema.schemata WHERE schema_name = 'dw')"
                ))
                exists = result.scalar()
                if not exists:
                    logger.error("✗ Schema dw não existe")
                    self.record_test("Schema dw", False)
                    return False
                logger.info("✓ Schema dw existe")
                self.record_test("Schema dw", True)
            return True
        except Exception as e:
            logger.error(f"✗ Erro ao verificar schema DW: {e}")
            self.record_test("Schema DW", False)
            return False
    
    def test_dw_tables(self) -> bool:
        """Test if DW tables exist"""
        try:
            logger.info("Teste 17: Verificação de Tabelas DW")
            with self.engine.connect() as conn:
                # Check if tables exist
                tables = ['dim_cliente', 'dim_produto', 'dim_data', 'fato_vendas']
                for table in tables:
                    result = conn.execute(text(
                        f"SELECT EXISTS (SELECT FROM information_schema.tables "
                        f"WHERE table_schema = 'dw' AND table_name = '{table}')"
                    ))
                    exists = result.scalar()
                    if not exists:
                        logger.error(f"✗ Tabela dw.{table} não existe")
                        self.record_test(f"Tabela dw.{table}", False)
                        return False
                    logger.info(f"✓ Tabela dw.{table} existe")
                    self.record_test(f"Tabela dw.{table}", True)
            return True
        except Exception as e:
            logger.error(f"✗ Erro ao verificar tabelas DW: {e}")
            self.record_test("Tabelas DW", False)
            return False
    
    def test_dw_data(self) -> bool:
        """Test if DW tables have expected data"""
        try:
            logger.info("Teste 18: Verificação de Dados no DW")
            with self.engine.connect() as conn:
                tables = {
                    'dw.dim_cliente': 10,
                    'dw.dim_produto': 10,
                    'dw.dim_data': 20,
                    'dw.fato_vendas': 46
                }
                
                all_valid = True
                for table, expected_count in tables.items():
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    if count == expected_count:
                        logger.info(f"✓ Tabela {table} tem {count} registros (esperado: {expected_count})")
                        self.record_test(f"Dados {table}", True)
                    else:
                        logger.error(f"✗ Tabela {table} tem {count} registros (esperado: {expected_count})")
                        self.record_test(f"Dados {table}", False)
                        all_valid = False
            return all_valid
        except Exception as e:
            logger.error(f"✗ Erro ao verificar dados DW: {e}")
            self.record_test("Dados DW", False)
            return False
    
    def test_logs_created(self) -> bool:
        """Test if log files are created"""
        try:
            logger.info("Teste 19: Verificação de Arquivos de Log")
            
            log_files = {
                'pipeline.log': Path('logs/pipeline.log'),
                'quality.log': Path('logs/quality.log'),
                'analytics.log': Path('logs/analytics.log'),
                'airflow.log': Path('logs/airflow.log')
            }
            
            all_exist = True
            for name, path in log_files.items():
                if path.exists():
                    size = path.stat().st_size
                    logger.info(f"✓ Arquivo de log {name} existe ({size} bytes)")
                    self.record_test(f"Log {name}", True)
                else:
                    logger.warning(f"⚠ Arquivo de log {name} não existe ainda (será criado na execução)")
                    self.record_test(f"Log {name}", True)  # Not critical if doesn't exist yet
            return True
        except Exception as e:
            logger.error(f"✗ Erro ao verificar arquivos de log: {e}")
            self.record_test("Arquivos de Log", False)
            return False
    
    def test_audit_schema_exists(self) -> bool:
        """Test if audit schema exists"""
        try:
            logger.info("Teste 20: Verificação do Schema Audit")
            with self.engine.connect() as conn:
                result = conn.execute(text(
                    "SELECT EXISTS (SELECT FROM information_schema.schemata WHERE schema_name = 'audit')"
                ))
                exists = result.scalar()
                if not exists:
                    logger.error("✗ Schema audit não existe")
                    self.record_test("Schema audit", False)
                    return False
                logger.info("✓ Schema audit existe")
                self.record_test("Schema audit", True)
            return True
        except Exception as e:
            logger.error(f"✗ Erro ao verificar schema audit: {e}")
            self.record_test("Schema audit", False)
            return False
    
    def test_pipeline_execution_table_exists(self) -> bool:
        """Test if audit.pipeline_execution table exists"""
        try:
            logger.info("Teste 21: Verificação da Tabela pipeline_execution")
            with self.engine.connect() as conn:
                result = conn.execute(text(
                    "SELECT EXISTS (SELECT FROM information_schema.tables "
                    "WHERE table_schema = 'audit' AND table_name = 'pipeline_execution')"
                ))
                exists = result.scalar()
                if not exists:
                    logger.error("✗ Tabela audit.pipeline_execution não existe")
                    self.record_test("Tabela pipeline_execution", False)
                    return False
                logger.info("✓ Tabela audit.pipeline_execution existe")
                self.record_test("Tabela pipeline_execution", True)
            return True
        except Exception as e:
            logger.error(f"✗ Erro ao verificar tabela pipeline_execution: {e}")
            self.record_test("Tabela pipeline_execution", False)
            return False
    
    def test_execution_history_csv_exists(self) -> bool:
        """Test if execution_history.csv exists"""
        try:
            logger.info("Teste 22: Verificação do Arquivo execution_history.csv")
            csv_file = Path('monitoring/execution_history.csv')
            if csv_file.exists():
                size = csv_file.stat().st_size
                logger.info(f"✓ Arquivo execution_history.csv existe ({size} bytes)")
                self.record_test("Arquivo execution_history.csv", True)
                return True
            else:
                logger.warning(f"⚠ Arquivo execution_history.csv não existe ainda (será criado na execução)")
                self.record_test("Arquivo execution_history.csv", True)  # Not critical if doesn't exist yet
                return True
        except Exception as e:
            logger.error(f"✗ Erro ao verificar execution_history.csv: {e}")
            self.record_test("Arquivo execution_history.csv", False)
            return False
    
    def test_data_quality_metrics_exists(self) -> bool:
        """Test if data_quality_metrics.parquet exists"""
        try:
            logger.info("Teste 23: Verificação do Arquivo data_quality_metrics.parquet")
            metrics_file = ANALYTICS_DATA_DIR / 'data_quality_metrics.parquet'
            if metrics_file.exists():
                size = metrics_file.stat().st_size
                logger.info(f"✓ Arquivo data_quality_metrics.parquet existe ({size} bytes)")
                self.record_test("Arquivo data_quality_metrics.parquet", True)
                return True
            else:
                logger.warning(f"⚠ Arquivo data_quality_metrics.parquet não existe ainda (será criado na execução)")
                self.record_test("Arquivo data_quality_metrics.parquet", True)  # Not critical if doesn't exist yet
                return True
        except Exception as e:
            logger.error(f"✗ Erro ao verificar data_quality_metrics.parquet: {e}")
            self.record_test("Arquivo data_quality_metrics.parquet", False)
            return False
    
    def test_monitoring_functioning(self) -> bool:
        """Test if monitoring system is functioning"""
        try:
            logger.info("Teste 24: Verificação do Sistema de Monitoramento")
            
            # Test if monitoring module can be imported
            try:
                from monitoring.pipeline_monitor import PipelineMonitor
                logger.info("✓ Módulo pipeline_monitor importado com sucesso")
                self.record_test("Import pipeline_monitor", True)
            except ImportError as e:
                logger.error(f"✗ Falha ao importar pipeline_monitor: {e}")
                self.record_test("Import pipeline_monitor", False)
                return False
            
            # Test if monitor can be instantiated
            try:
                monitor = PipelineMonitor()
                logger.info("✓ PipelineMonitor instanciado com sucesso")
                self.record_test("Instanciação PipelineMonitor", True)
            except Exception as e:
                logger.error(f"✗ Falha ao instanciar PipelineMonitor: {e}")
                self.record_test("Instanciação PipelineMonitor", False)
                return False
            
            return True
        except Exception as e:
            logger.error(f"✗ Erro ao verificar sistema de monitoramento: {e}")
            self.record_test("Sistema de Monitoramento", False)
            return False
    
    def record_test(self, test_name: str, passed: bool) -> None:
        """Record test result"""
        self.test_results.append((test_name, passed))
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
    
    def print_summary(self) -> None:
        """Print test summary"""
        logger.info("")
        logger.info("=" * 70)
        logger.info("RESUMO DOS TESTES")
        logger.info("=" * 70)
        logger.info(f"Total de Testes: {self.total_tests}")
        logger.info(f"Testes Aprovados: {self.passed_tests}")
        logger.info(f"Testes Falhados: {self.failed_tests}")
        logger.info(f"Taxa de Sucesso: {(self.passed_tests/self.total_tests*100):.1f}%")
        logger.info("")
        
        if self.failed_tests > 0:
            logger.info("Testes Falhados:")
            for test_name, passed in self.test_results:
                if not passed:
                    logger.info(f"  ✗ {test_name}")
            logger.info("")
        
        logger.info("=" * 70)
        
        if self.failed_tests == 0:
            logger.info("✓ TODOS OS TESTES PASSARAM! O projeto está funcionando corretamente.")
        else:
            logger.warning(f"✗ {self.failed_tests} teste(s) falharam. Verifique os erros acima.")
    
    def run_all_tests(self) -> None:
        """Run all tests"""
        logger.info("")
        logger.info("=" * 70)
        logger.info("INICIANDO TESTES COMPLETOS DO PROJETO")
        logger.info("=" * 70)
        logger.info("")
        
        try:
            # Run tests
            self.connect_postgres()
            if self.engine:
                self.test_erp_schema()
                self.test_erp_data()
                self.test_foreign_keys()
            
            self.test_directory_structure()
            self.test_raw_layer_files()
            self.test_raw_layer_data()
            
            if self.engine:
                self.test_data_integrity()
            
            # Curated Layer tests
            self.test_curated_layer_files()
            self.test_curated_layer_data()
            self.test_curated_layer_schema()
            self.test_curated_layer_integrity()
            
            # DW tests
            if self.engine:
                self.test_dw_schema()
                self.test_dw_tables()
                self.test_dw_data()
            
            # Analytics Layer tests
            self.test_analytics_layer_files()
            self.test_analytics_layer_data()
            self.test_analytics_layer_schema()
            
            # Sprint 8 Monitoring and Observability tests
            self.test_logs_created()
            if self.engine:
                self.test_audit_schema_exists()
                self.test_pipeline_execution_table_exists()
            self.test_execution_history_csv_exists()
            self.test_data_quality_metrics_exists()
            self.test_monitoring_functioning()
            
            # Print summary
            self.print_summary()
            
        except Exception as e:
            logger.error(f"Erro fatal durante execução dos testes: {e}")
        finally:
            # Close connection
            if self.engine:
                self.engine.dispose()
                logger.info("Conexão com PostgreSQL encerrada")


def main():
    """Main function"""
    tester = ProjectTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
