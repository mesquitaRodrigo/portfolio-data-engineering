"""
Data Warehouse Loader Script
Loads data from Curated Layer (Parquet) to PostgreSQL Data Warehouse (dw schema)
Sprint 6 - Materialização do Data Warehouse no PostgreSQL
"""

import sys
import logging
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent.parent))
from config.settings import (
    DATABASE_URL,
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


class DWLoader:
    """Loads data from Curated Layer to PostgreSQL Data Warehouse"""
    
    def __init__(self):
        self.engine = None
    
    def connect(self) -> bool:
        """Connect to PostgreSQL database"""
        try:
            logger.info("Conectando ao PostgreSQL...")
            self.engine = create_engine(DATABASE_URL)
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("✓ Conexão estabelecida com sucesso")
            return True
        except Exception as e:
            logger.error(f"✗ Erro ao conectar ao PostgreSQL: {e}")
            return False
    
    def execute_ddl(self) -> bool:
        """Execute DDL script to create DW schema and tables"""
        try:
            logger.info("Executando script DDL do Data Warehouse...")
            
            ddl_path = Path(__file__).parent.parent.parent / "sql" / "dw" / "create_dw_schema.sql"
            
            if not ddl_path.exists():
                logger.error(f"✗ Arquivo DDL não encontrado: {ddl_path}")
                return False
            
            with open(ddl_path, 'r') as f:
                ddl_script = f.read()
            
            with self.engine.connect() as conn:
                conn.execute(text(ddl_script))
                conn.commit()
            
            logger.info("✓ Schema e tabelas do DW criados com sucesso")
            return True
        except Exception as e:
            logger.error(f"✗ Erro ao executar DDL: {e}")
            return False
    
    def load_dim_cliente(self) -> bool:
        """Load dim_cliente from Parquet to PostgreSQL"""
        try:
            logger.info("Carregando dim_cliente...")
            
            if not CURATED_DIM_CLIENTE_FILE.exists():
                logger.error(f"✗ Arquivo não encontrado: {CURATED_DIM_CLIENTE_FILE}")
                return False
            
            df = pd.read_parquet(CURATED_DIM_CLIENTE_FILE)
            logger.info(f"  Lidos {len(df)} registros do arquivo Parquet")
            
            # Truncate existing data
            with self.engine.connect() as conn:
                conn.execute(text("TRUNCATE TABLE dw.dim_cliente CASCADE"))
                conn.commit()
            
            # Load data
            df.to_sql('dim_cliente', self.engine, schema='dw', if_exists='append', index=False)
            
            logger.info(f"✓ dim_cliente carregada com {len(df)} registros")
            return True
        except Exception as e:
            logger.error(f"✗ Erro ao carregar dim_cliente: {e}")
            return False
    
    def load_dim_produto(self) -> bool:
        """Load dim_produto from Parquet to PostgreSQL"""
        try:
            logger.info("Carregando dim_produto...")
            
            if not CURATED_DIM_PRODUTO_FILE.exists():
                logger.error(f"✗ Arquivo não encontrado: {CURATED_DIM_PRODUTO_FILE}")
                return False
            
            df = pd.read_parquet(CURATED_DIM_PRODUTO_FILE)
            logger.info(f"  Lidos {len(df)} registros do arquivo Parquet")
            
            # Truncate existing data
            with self.engine.connect() as conn:
                conn.execute(text("TRUNCATE TABLE dw.dim_produto CASCADE"))
                conn.commit()
            
            # Load data
            df.to_sql('dim_produto', self.engine, schema='dw', if_exists='append', index=False)
            
            logger.info(f"✓ dim_produto carregada com {len(df)} registros")
            return True
        except Exception as e:
            logger.error(f"✗ Erro ao carregar dim_produto: {e}")
            return False
    
    def load_dim_data(self) -> bool:
        """Load dim_data from Parquet to PostgreSQL"""
        try:
            logger.info("Carregando dim_data...")
            
            if not CURATED_DIM_DATA_FILE.exists():
                logger.error(f"✗ Arquivo não encontrado: {CURATED_DIM_DATA_FILE}")
                return False
            
            df = pd.read_parquet(CURATED_DIM_DATA_FILE)
            logger.info(f"  Lidos {len(df)} registros do arquivo Parquet")
            
            # Convert datetime to date if needed
            if 'data' in df.columns:
                df['data'] = pd.to_datetime(df['data']).dt.date
            
            # Truncate existing data
            with self.engine.connect() as conn:
                conn.execute(text("TRUNCATE TABLE dw.dim_data CASCADE"))
                conn.commit()
            
            # Load data
            df.to_sql('dim_data', self.engine, schema='dw', if_exists='append', index=False)
            
            logger.info(f"✓ dim_data carregada com {len(df)} registros")
            return True
        except Exception as e:
            logger.error(f"✗ Erro ao carregar dim_data: {e}")
            return False
    
    def load_fato_vendas(self) -> bool:
        """Load fato_vendas from Parquet to PostgreSQL"""
        try:
            logger.info("Carregando fato_vendas...")
            
            if not CURATED_FATO_VENDAS_FILE.exists():
                logger.error(f"✗ Arquivo não encontrado: {CURATED_FATO_VENDAS_FILE}")
                return False
            
            df = pd.read_parquet(CURATED_FATO_VENDAS_FILE)
            logger.info(f"  Lidos {len(df)} registros do arquivo Parquet")
            
            # Convert data_pedido to date if needed
            if 'data_pedido' in df.columns:
                df['data_pedido'] = pd.to_datetime(df['data_pedido']).dt.date
            
            # Truncate existing data
            with self.engine.connect() as conn:
                conn.execute(text("TRUNCATE TABLE dw.fato_vendas CASCADE"))
                conn.commit()
            
            # Load data
            df.to_sql('fato_vendas', self.engine, schema='dw', if_exists='append', index=False)
            
            logger.info(f"✓ fato_vendas carregada com {len(df)} registros")
            return True
        except Exception as e:
            logger.error(f"✗ Erro ao carregar fato_vendas: {e}")
            return False
    
    def verify_load(self) -> bool:
        """Verify that all tables were loaded correctly"""
        try:
            logger.info("Verificando carregamento das tabelas...")
            
            with self.engine.connect() as conn:
                # Check dim_cliente
                result = conn.execute(text("SELECT COUNT(*) FROM dw.dim_cliente"))
                count = result.scalar()
                logger.info(f"  dw.dim_cliente: {count} registros")
                
                # Check dim_produto
                result = conn.execute(text("SELECT COUNT(*) FROM dw.dim_produto"))
                count = result.scalar()
                logger.info(f"  dw.dim_produto: {count} registros")
                
                # Check dim_data
                result = conn.execute(text("SELECT COUNT(*) FROM dw.dim_data"))
                count = result.scalar()
                logger.info(f"  dw.dim_data: {count} registros")
                
                # Check fato_vendas
                result = conn.execute(text("SELECT COUNT(*) FROM dw.fato_vendas"))
                count = result.scalar()
                logger.info(f"  dw.fato_vendas: {count} registros")
            
            logger.info("✓ Verificação concluída com sucesso")
            return True
        except Exception as e:
            logger.error(f"✗ Erro ao verificar carregamento: {e}")
            return False
    
    def run(self) -> bool:
        """Execute the complete DW loading process"""
        logger.info("")
        logger.info("=" * 70)
        logger.info("LOAD DW POSTGRESQL - CURATED LAYER → DATA WAREHOUSE")
        logger.info("=" * 70)
        logger.info("")
        
        # Connect to database
        if not self.connect():
            return False
        
        # Execute DDL
        if not self.execute_ddl():
            return False
        
        # Load all tables
        success = True
        success = success and self.load_dim_cliente()
        success = success and self.load_dim_produto()
        success = success and self.load_dim_data()
        success = success and self.load_fato_vendas()
        
        # Verify load
        if success:
            self.verify_load()
        
        # Close connection
        if self.engine:
            self.engine.dispose()
            logger.info("Conexão com PostgreSQL encerrada")
        
        logger.info("")
        if success:
            logger.info("✓ LOAD DW CONCLUÍDO COM SUCESSO!")
        else:
            logger.error("✗ LOAD DW FALHOU!")
        
        logger.info("=" * 70)
        logger.info("")
        
        return success


def main():
    """Main function"""
    loader = DWLoader()
    success = loader.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
