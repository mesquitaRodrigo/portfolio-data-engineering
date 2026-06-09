# Portfolio Data Engineering Project

A complete data engineering portfolio project demonstrating a modern layered architecture inspired by Data Lake + Data Warehouse patterns. This project implements a professional data pipeline with PostgreSQL, Python, Pandas, DuckDB, and Parquet for business analytics.

## 📋 Overview

This project implements a complete data pipeline following best practices of modern data engineering:
- **ERP (PostgreSQL)**: Operational system (OLTP) - clientes, produtos, pedidos, itens_pedido
- **Extract**: Data extraction from ERP to Raw Layer (Parquet)
- **Raw Layer**: Immutable data lake storage (data/raw/)
- **Transform**: Data transformation to dimensional model (Star Schema)
- **Curated Layer**: Data warehouse with dim_cliente, dim_produto, fato_vendas (data/curated/)
- **DuckDB**: High-performance analytical queries on Parquet files
- **Analytics**: Business metrics and insights (data/analytics/)

**Key Principle**: No analytics queries are performed directly on the ERP. All analyses read from the Curated Layer.

## 🏗️ Architecture

### Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         ERP (PostgreSQL)                         │
│                    Sistema Operacional (OLTP)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────────┐  │
│  │ clientes │  │ produtos │  │ pedidos  │  │ itens_pedido  │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                        [EXTRACT]
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      RAW LAYER (Data Lake)                       │
│                   Arquivos Parquet Brutos                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────────┐  │
│  │ clientes │  │ produtos │  │ pedidos  │  │ itens_pedido  │  │
│  │.parquet  │  │.parquet  │  │.parquet  │  │  .parquet     │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                       [TRANSFORM]
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   CURATED LAYER (Data Warehouse)                │
│                  Modelo Dimensional (Star Schema)                │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │ dim_cliente  │  │ dim_produto  │  │   fato_vendas       │   │
│  │   .parquet   │  │   .parquet   │  │     .parquet        │   │
│  └──────────────┘  └──────────────┘  └────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                         [LOAD]
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                       DuckDB (Analytics)                         │
│                  Banco de Dados Analítico (OLAP)                │
│                   Consultas em Memória                           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                        [ANALYTICS]
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   ANALYTICS LAYER (Métricas)                     │
│                   Resultados de Análises                        │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │ receita_total│  │ receita_por  │  │ produto_mais_      │   │
│  │   .parquet   │  │  cliente     │  │ vendido.parquet    │   │
│  └──────────────┘  └──────────────┘  └────────────────────┘   │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │ receita_por  │  │ receita_por  │  │ ticket_medio       │   │
│  │  produto     │  │  cidade      │  │ .parquet           │   │
│  └──────────────┘  └──────────────┘  └────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

| Layer | Purpose | Technology | Read-Only |
|-------|---------|------------|-----------|
| **ERP** | Operational system (OLTP) | PostgreSQL | No |
| **Raw** | Immutable data lake | Parquet | Yes |
| **Curated** | Dimensional model (OLAP) | Parquet | Yes |
| **Analytics** | Business metrics | Parquet | Yes |

## 🛠️ Technologies Used

- **PostgreSQL 15**: Operational system (OLTP) database
- **Docker & Docker Compose**: Containerization and orchestration
- **Python 3.8+**: Programming language for ETL and analytics
- **SQLAlchemy**: SQL toolkit and ORM for ERP connection
- **Pandas**: Data manipulation and transformation
- **DuckDB**: High-performance analytical database for Curated Layer queries
- **PyArrow**: Parquet file format support
- **psycopg2-binary**: PostgreSQL adapter for Python

## 📁 Project Structure

```
portfolio-data-engineering/
├── analytics/                      # Analytics Python scripts
│   ├── receita_total.py           # Total revenue analysis
│   ├── receita_por_cliente.py     # Revenue by client analysis
│   ├── receita_por_produto.py     # Revenue by product analysis
│   ├── receita_por_cidade.py      # Revenue by city analysis
│   ├── ticket_medio.py           # Average ticket analysis
│   └── produto_mais_vendido.py   # Most sold product analysis
│
├── config/
│   └── settings.py                # Centralized configuration
│
├── data/
│   ├── raw/                       # Raw Layer (Data Lake)
│   │   ├── clientes.parquet       # Extracted from ERP
│   │   ├── produtos.parquet       # Extracted from ERP
│   │   ├── pedidos.parquet        # Extracted from ERP
│   │   └── itens_pedido.parquet   # Extracted from ERP
│   │
│   ├── curated/                   # Curated Layer (Data Warehouse)
│   │   ├── dim_cliente.parquet    # Customer dimension
│   │   ├── dim_produto.parquet    # Product dimension
│   │   ├── dim_data.parquet       # Date dimension
│   │   └── fato_vendas.parquet    # Sales fact table
│   │
│   └── analytics/                 # Analytics Layer (Metrics)
│       ├── receita_total.parquet
│       ├── receita_por_cliente.parquet
│       ├── receita_por_produto.parquet
│       ├── receita_por_cidade.parquet
│       ├── ticket_medio.parquet
│       └── produto_mais_vendido.parquet
│
├── docker/                        # Docker configurations
│
├── docs/                          # Documentation
│   ├── arquitetura.md             # Architecture documentation
│   └── modelo_dados.md            # Data model documentation
│
├── etl/                           # ETL Pipeline
│   ├── extract/                   # Extract: ERP → Raw Layer
│   │   ├── extract_clientes.py
│   │   ├── extract_produtos.py
│   │   ├── extract_pedidos.py
│   │   └── extract_itens_pedido.py
│   │
│   ├── transform/                 # Transform: Raw → Curated
│   │   └── build_curated_layer.py
│   │
│   └── load/                      # Load: Curated → DuckDB
│       └── load_duckdb.py
│
├── sql/                           # SQL Scripts
│   ├── ddl/                       # Database Schema (ERP)
│   │   ├── create_erp_schema.sql  # Complete ERP schema DDL
│   │   ├── load_sample_data.sql   # Sample data load script
│   │   ├── clientes.sql
│   │   ├── produtos.sql
│   │   ├── pedidos.sql
│   │   └── itens_pedido.sql
│   │
│   ├── extract/                   # Extract Queries
│   │   ├── clientes.sql
│   │   ├── produtos.sql
│   │   ├── pedidos.sql
│   │   └── itens_pedido.sql
│   │
│   ├── transform/                 # Transform Queries
│   │   ├── dim_cliente.sql
│   │   ├── dim_produto.sql
│   │   └── fato_vendas.sql
│   │
│   ├── analytics/                 # Analytics Queries
│   │   ├── fato_vendas.sql        # Base analytical query
│   │   ├── receita_total.sql
│   │   ├── receita_por_cliente.sql
│   │   ├── receita_por_produto.sql
│   │   ├── receita_por_cidade.sql
│   │   ├── ticket_medio.sql
│   │   └── produto_mais_vendido.sql
│   │
│   └── validation/                # Validation Queries
│       ├── count_clientes.sql
│       ├── count_produtos.sql
│       ├── count_pedidos.sql
│       └── count_itens_pedido.sql
│
├── docker-compose.yml              # PostgreSQL container configuration
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── .gitignore                      # Git ignore rules
```

## 🗄️ Data Model

### ERP Operational Model (PostgreSQL - OLTP)

The ERP follows a normalized relational model designed for transactional operations:

**clientes**
- `id_cliente`: Primary key
- `nome`: Customer name
- `cidade`: Customer city

**produtos**
- `id_produto`: Primary key
- `nome`: Product name
- `categoria`: Product category
- `preco`: Product price

**pedidos**
- `id_pedido`: Primary key
- `id_cliente`: Foreign key to clientes
- `data_pedido`: Order date

**itens_pedido**
- `id_item`: Primary key
- `id_pedido`: Foreign key to pedidos
- `id_produto`: Foreign key to produtos
- `quantidade`: Quantity sold
- `preco_unitario`: Unit price at sale

### ERP Relationships

- **clientes (1:N) pedidos**: One customer can place multiple orders
- **pedidos (1:N) itens_pedido**: One order can contain multiple items
- **produtos (1:N) itens_pedido**: One product can appear in multiple order items

### ERP Architecture

The ERP is designed as a pure operational system (OLTP) with:
- **3NF Normalization**: Eliminates data redundancy
- **Foreign Key Constraints**: Ensures referential integrity
- **Indexes**: Optimized for transactional performance
- **No Analytics**: All analytical queries read from Curated Layer only

### Data Flow: ERP → Raw → Curated → Analytics

1. **ERP (PostgreSQL)**: Operational system where transactions occur
2. **Extract**: Data extracted from ERP to Raw Layer (Parquet files)
3. **Raw Layer**: Immutable data lake storage preserving original ERP state
4. **Transform**: Raw data transformed to dimensional model (Star Schema)
5. **Curated Layer**: Data warehouse with dim_cliente, dim_produto, fato_vendas
6. **DuckDB**: High-performance analytical queries on Curated Layer
7. **Analytics**: Business metrics and insights generated from Curated Layer

### Curated Layer (Data Warehouse - OLAP)

The Curated Layer implements a Star Schema dimensional model optimized for analytical queries. Data is transformed from the Raw Layer into dimension tables and a fact table.

**Star Schema Diagram**

```
        dim_cliente
             │
             │
             ▼
        fato_vendas
             ▲
             │
             │
        dim_produto
             ▲
             │
             │
        dim_data
```

**dim_cliente** (Customer Dimension)
- `id_cliente`: Primary key (natural key from ERP)
- `nome`: Customer name
- `cidade`: Customer city

**dim_produto** (Product Dimension)
- `id_produto`: Primary key (natural key from ERP)
- `nome`: Product name
- `categoria`: Product category
- `preco`: Product price

**dim_data** (Date Dimension)
- `data`: Date (primary key)
- `ano`: Year
- `mes`: Month (1-12)
- `dia`: Day of month
- `trimestre`: Quarter (1-4)
- `nome_mes`: Month name in Portuguese

**fato_vendas** (Sales Fact Table)
- `id_pedido`: Order ID (natural key from ERP)
- `data_pedido`: Order date
- `id_cliente`: Foreign key to dim_cliente
- `id_produto`: Foreign key to dim_produto
- `quantidade`: Quantity sold
- `preco_unitario`: Unit price at sale
- `valor_total`: Total sale value (quantidade * preco_unitario)

### Relationships
- `fato_vendas.id_cliente` → `dim_cliente.id_cliente`
- `fato_vendas.id_produto` → `dim_produto.id_produto`
- `fato_vendas.data_pedido` → `dim_data.data`

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Python 3.8 or higher
- Git

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd portfolio-data-engineering
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## 🐳 Running PostgreSQL with Docker

1. **Start PostgreSQL container**
```bash
docker-compose up -d
```

2. **Verify PostgreSQL is running**
```bash
docker-compose ps
```

3. **Check logs if needed**
```bash
docker-compose logs postgres
```

4. **Stop PostgreSQL**
```bash
docker-compose down
```

The PostgreSQL database will be available at:
- Host: localhost
- Port: 5432
- Database: portfolio_db
- User: admin
- Password: admin123

## �️ Setting Up the ERP Schema

### Step 1: Create ERP Schema

Execute the complete ERP schema DDL:

```bash
psql -h localhost -U admin -d portfolio_db -f sql/ddl/create_erp_schema.sql
```

This creates:
- `clientes` table with PK and constraints
- `produtos` table with PK and constraints
- `pedidos` table with FK to clientes
- `itens_pedido` table with FKs to pedidos and produtos
- All necessary indexes for performance
- Check constraints for data integrity

### Step 2: Load Sample Data

Load sample data for testing and development:

```bash
psql -h localhost -U admin -d portfolio_db -f sql/ddl/load_sample_data.sql
```

This inserts:
- 10 clientes
- 10 produtos
- 20 pedidos
- 50 itens_pedido

### Step 3: Validate Data

Run validation queries to verify data integrity:

```bash
psql -h localhost -U admin -d portfolio_db -f sql/validation/count_clientes.sql
psql -h localhost -U admin -d portfolio_db -f sql/validation/count_produtos.sql
psql -h localhost -U admin -d portfolio_db -f sql/validation/count_pedidos.sql
psql -h localhost -U admin -d portfolio_db -f sql/validation/count_itens_pedido.sql
```

### Step 4: Test Analytical Base Query

Verify the analytical base query (fato_vendas):

```bash
psql -h localhost -U admin -d portfolio_db -f sql/analytics/fato_vendas.sql
```

This query represents the future fato_vendas table in the Data Warehouse, returning:
- id_pedido, data_pedido, id_cliente, cliente, cidade
- id_produto, produto, categoria
- quantidade, preco_unitario, valor_total

## Sprint 2 - Raw Layer (Data Lake)

### Overview

The Raw Layer is the first stage in the data pipeline, serving as an immutable copy of the ERP operational data. Data is extracted from PostgreSQL and stored in Parquet format without any transformations.

### Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         ERP (PostgreSQL)                         │
│                    Sistema Operacional (OLTP)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────────┐  │
│  │ clientes │  │ produtos │  │ pedidos  │  │ itens_pedido  │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                        [EXTRACT]
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      RAW LAYER (Data Lake)                       │
│                   Arquivos Parquet Brutos                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────────┐  │
│  │ clientes │  │ produtos │  │ pedidos  │  │ itens_pedido  │  │
│  │.parquet  │  │.parquet  │  │.parquet  │  │  .parquet     │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Raw Layer Characteristics

- **Immutable**: Data is never modified after extraction
- **Append-only**: New extractions add data without overwriting
- **No Transformations**: Data remains in its original ERP state
- **Parquet Format**: Columnar storage for efficient compression and query performance
- **Source of Truth**: Serves as the authoritative copy of ERP data

### Raw Layer Files

Located in `data/raw/`:

- **clientes.parquet**: Customer data extracted from ERP
- **produtos.parquet**: Product data extracted from ERP
- **pedidos.parquet**: Order data extracted from ERP
- **itens_pedido.parquet**: Order item data extracted from ERP

### Extraction Process

The extraction is performed by `etl/extract/extract_all_tables.py`, which:

1. Connects to PostgreSQL using configuration from `config/settings.py`
2. Extracts all four ERP tables (clientes, produtos, pedidos, itens_pedido)
3. Saves each table as a Parquet file in `data/raw/`
4. Generates extraction statistics and logs
5. Handles errors gracefully with proper connection cleanup

### Running the Extraction

Execute the extraction script:

```bash
python3 etl/extract/extract_all_tables.py
```

**Expected Output:**

```
[INFO] Conectando ao PostgreSQL: localhost:5432/portfolio_db
[INFO] Conexão estabelecida com sucesso
[INFO] ============================================================
[INFO] Iniciando extração do ERP para Raw Layer
[INFO] ============================================================
[INFO] Extraindo tabela: clientes
[INFO] 10 registros extraídos de clientes
[INFO] Arquivo salvo: data/raw/clientes.parquet
[INFO] Extraindo tabela: produtos
[INFO] 10 registros extraídos de produtos
[INFO] Arquivo salvo: data/raw/produtos.parquet
[INFO] Extraindo tabela: pedidos
[INFO] 20 registros extraídos de pedidos
[INFO] Arquivo salvo: data/raw/pedidos.parquet
[INFO] Extraindo tabela: itens_pedido
[INFO] 50 registros extraídos de itens_pedido
[INFO] Arquivo salvo: data/raw/itens_pedido.parquet
[INFO] ============================================================
[INFO] Extração concluída com sucesso
[INFO] ============================================================

Estatísticas de Extração
----------------------------------------
Tabela          | Registros  
----------------------------------------
clientes        | 10        
produtos        | 10        
pedidos         | 20        
itens_pedido    | 50        
----------------------------------------
TOTAL           | 90        

Arquivos salvos em: data/raw
```

### Key Features

- **Centralized Configuration**: All database credentials and paths from `config/settings.py`
- **Reusable Functions**: `connect_postgres()`, `extract_table()`, `save_parquet()`
- **Error Handling**: Comprehensive try/except blocks with friendly error messages
- **Logging**: Informative logs at each step of the extraction process
- **Statistics**: Summary table showing records extracted per table
- **Safe Connection**: Proper connection cleanup with `finally` block


## Sprint 3 - Curated Layer (Mini Data Warehouse)

### Overview

The Curated Layer transforms the Raw Layer data into a dimensional model (Star Schema) optimized for analytics. This layer represents a simplified Data Warehouse that serves as the foundation for all analytical queries.

### Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      RAW LAYER (Data Lake)                       │
│                   Arquivos Parquet Brutos                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────────┐  │
│  │ clientes │  │ produtos │  │ pedidos  │  │ itens_pedido  │  │
│  │.parquet  │  │.parquet  │  │.parquet  │  │  .parquet     │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                       [TRANSFORM]
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   CURATED LAYER (Data Warehouse)                │
│                  Modelo Dimensional (Star Schema)                │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │ dim_cliente  │  │ dim_produto  │  │   fato_vendas       │   │
│  │   .parquet   │  │   .parquet   │  │     .parquet        │   │
│  └──────────────┘  └──────────────┘  └────────────────────┘   │
│  ┌──────────────┐                                              │
│  │  dim_data    │                                              │
│  │   .parquet   │                                              │
│  └──────────────┘                                              │
└─────────────────────────────────────────────────────────────────┘
```

### Curated Layer Characteristics

- **Star Schema**: Optimized dimensional model for analytics
- **Denormalized Dimensions**: Dimension tables contain descriptive attributes
- **Fact Table**: Central fact table with foreign keys to dimensions
- **Calculated Metrics**: valor_total calculated as quantidade * preco_unitario
- **Date Dimension**: Automatically generated from order dates
- **Analytics-Ready**: Optimized for DuckDB and analytical queries

### Dimensional Model

**Star Schema**

```
        dim_cliente
             │
             │
             ▼
        fato_vendas
             ▲
             │
             │
        dim_produto
             ▲
             │
             │
        dim_data
```

**dim_cliente** (Customer Dimension)
- Source: `data/raw/clientes.parquet`
- Fields: `id_cliente`, `nome`, `cidade`
- Purpose: Customer master data for analytics

**dim_produto** (Product Dimension)
- Source: `data/raw/produtos.parquet`
- Fields: `id_produto`, `nome`, `categoria`, `preco`
- Purpose: Product master data for analytics

**dim_data** (Date Dimension)
- Source: Generated from `data/raw/pedidos.parquet` (unique dates)
- Fields: `data`, `ano`, `mes`, `dia`, `trimestre`, `nome_mes`
- Purpose: Time-based analysis (year, month, quarter, day)

**fato_vendas** (Sales Fact Table)
- Source: Join of `data/raw/pedidos.parquet` + `data/raw/itens_pedido.parquet`
- Fields: `id_pedido`, `data_pedido`, `id_cliente`, `id_produto`, `quantidade`, `preco_unitario`, `valor_total`
- Calculation: `valor_total = quantidade * preco_unitario`
- Purpose: Central fact table for sales analytics

### Transformation Process

The transformation is performed by `etl/transform/build_curated_layer.py`, which:

1. **Creates dim_cliente**: Selects customer data from Raw Layer
2. **Creates dim_produto**: Selects product data from Raw Layer
3. **Creates dim_data**: Extracts unique dates from pedidos, generates date attributes
4. **Creates fato_vendas**: Joins pedidos with itens_pedido, calculates valor_total
5. **Saves all tables**: Writes Parquet files to `data/curated/`
6. **Generates statistics**: Logs record counts for each table

### Running the Transformation

Execute the transformation script:

```bash
python3 etl/transform/build_curated_layer.py
```

**Expected Output:**

```
============================================================
Building Curated Layer (Mini Data Warehouse)
============================================================

[INFO] Creating dim_cliente...
[INFO] dim_cliente: 10 registros
[INFO] Creating dim_produto...
[INFO] dim_produto: 10 registros
[INFO] Creating dim_data...
[INFO] dim_data: 20 registros
[INFO] Creating fato_vendas...
[INFO] fato_vendas: 46 registros

============================================================
Curated Layer built successfully!
============================================================

Generated files:
  - data/curated/dim_cliente.parquet
  - data/curated/dim_produto.parquet
  - data/curated/dim_data.parquet
  - data/curated/fato_vendas.parquet
```

### Key Features

- **Modular Design**: Each dimension/fact created in separate functions
- **Automatic Date Dimension**: Generated from existing order dates
- **Calculated Metrics**: valor_total computed on transformation
- **Data Validation**: Record counts logged for verification
- **Error Handling**: Proper exception handling and logging
- **Reproducible**: Deterministic transformation from Raw Layer

### Data Validation

After transformation, verify the generated files:

```bash
python3 -c "import pandas as pd; print('dim_cliente:', len(pd.read_parquet('data/curated/dim_cliente.parquet'))); print('dim_produto:', len(pd.read_parquet('data/curated/dim_produto.parquet'))); print('dim_data:', len(pd.read_parquet('data/curated/dim_data.parquet'))); print('fato_vendas:', len(pd.read_parquet('data/curated/fato_vendas.parquet')))"
```

### Next Steps

The Curated Layer is now ready for:
- **Sprint 4**: Analytics Layer with DuckDB queries
- Business metrics calculation
- Dashboard visualization
- Advanced analytics


### Key Features

- **Centralized Configuration**: All database credentials and paths from `config/settings.py`
- **Reusable Functions**: `connect_postgres()`, `extract_table()`, `save_parquet()`
- **Error Handling**: Comprehensive try/except blocks with friendly error messages
- **Logging**: Informative logs at each step of the extraction process
- **Statistics**: Summary table showing records extracted per table
- **Safe Connection**: Proper connection cleanup with `finally` block


## �🔄 Running the ETL Pipeline

### Complete Pipeline (Recommended)

Execute the complete pipeline with a single command:
```bash
python3 run_pipeline.py
```

This executes all steps in sequence:
1. **Extract**: ERP → Raw Layer
2. **Curated**: Raw Layer → Curated Layer
3. **Analytics**: Curated Layer → Analytics Layer
4. **Tests**: Validate all layers

### Individual Steps

#### Step 1: Extract (ERP → Raw Layer)

Extract data from ERP to Raw Layer:
```bash
python3 etl/extract/extract_all_tables.py
```

This extracts data from PostgreSQL and saves to `data/raw/` as Parquet files.

### Step 2: Transform (Raw → Curated)

Transform raw data to dimensional model:
```bash
python3 etl/transform/build_curated_layer.py
```

This transforms raw data to Star Schema and saves to `data/curated/`.

### Step 3: Analytics (Curated → Analytics)

Calculate business metrics:
```bash
python3 analytics/run_analytics.py
```

This calculates all business metrics and saves to `data/analytics/`.

#### Step 4: Tests

Validate all layers:
```bash
python3 test_project.py
```

This runs comprehensive tests on all data layers.

## 📊 Running Analytics

Execute analytics scripts using DuckDB on Curated Layer:

### Run All Analytics
```bash
python3 analytics/run_analytics.py
```
Executes all analytics metrics and generates a final report:
- Receita Total
- Receita por Cliente
- Receita por Produto
- Receita por Cidade
- Ticket Médio
- Produto Mais Vendido
- Top 5 Clientes
- Top 5 Produtos
- Receita Mensal

All analytics results are saved as Parquet files in `data/analytics/`.

### Individual Metrics

#### Receita Total
```bash
python3 analytics/receita_total.py
```
Calculates:
- Total revenue from all sales

#### Receita por Cliente
```bash
python3 analytics/receita_por_cliente.py
```
Calculates:
- Revenue per customer
- Results sorted by revenue (descending)

#### Receita por Produto
```bash
python3 analytics/receita_por_produto.py
```
Calculates:
- Revenue per product
- Results sorted by revenue (descending)

#### Receita por Cidade
```bash
python3 analytics/receita_por_cidade.py
```
Calculates:
- Revenue per city
- Results sorted by revenue (descending)

#### Ticket Médio
```bash
python3 analytics/ticket_medio.py
```
Calculates:
- Overall average ticket value

#### Produto Mais Vendido
```bash
python3 analytics/produto_mais_vendido.py
```
Identifies:
- Product with highest quantity sold
- Total quantity sold

#### Top 5 Clientes
```bash
python3 analytics/top_clientes.py
```
Identifies:
- Top 5 customers by revenue
- Revenue per customer

#### Top 5 Produtos
```bash
python3 analytics/top_produtos.py
```
Identifies:
- Top 5 products by quantity sold
- Total quantity sold

#### Receita Mensal
```bash
python3 analytics/receita_mensal.py
```
Calculates:
- Revenue by year and month
- Uses dim_data for date dimensions

## 🔧 Configuration

All configuration is centralized in `config/settings.py`:

- Database credentials (ERP - PostgreSQL)
- File paths for all layers (Raw, Curated, Analytics)
- Directory paths for ETL and SQL scripts
- SQL file paths for all operations

You can customize these settings without modifying the scripts.

## 📈 Business Metrics

The project calculates the following key metrics:

1. **Receita Total**: Total revenue from all sales
2. **Receita por Cliente**: Revenue breakdown by customer
3. **Receita por Produto**: Revenue breakdown by product
4. **Receita por Cidade**: Revenue breakdown by city
5. **Ticket Médio**: Average sale value
6. **Produto Mais Vendido**: Best-selling product by quantity
7. **Top 5 Clientes**: Top 5 customers by revenue
8. **Top 5 Produtos**: Top 5 products by quantity sold
9. **Receita Mensal**: Revenue by year and month

## � Documentation

- **[docs/arquitetura.md](docs/arquitetura.md)**: Detailed architecture documentation
- **[docs/modelo_dados.md](docs/modelo_dados.md)**: Data model documentation with ER diagrams

## �🔮 Future Enhancements

This project is prepared for future integration with:

### Orchestration
- **Apache Airflow**: Schedule and monitor ETL pipelines
- **Prefect**: Modern workflow orchestration
- **Dagster**: Data-aware orchestration

### Transformation
- **dbt**: Data transformation with version control
- **Great Expectations**: Data quality testing
- **Pandera**: Data validation

### Cloud Storage
- **AWS S3**: Scalable object storage
- **Azure Data Lake**: Enterprise data lake
- **MinIO**: S3-compatible local storage

### Visualization
- **Power BI**: Business intelligence dashboards
- **Streamlit**: Interactive dashboards
- **Apache Superset**: Open-source BI platform

### Advanced Analytics
- **Apache Spark**: Big data processing
- **Databricks**: Unified analytics platform
- **Snowflake**: Cloud data warehouse

### Monitoring
- **Prometheus**: Metrics monitoring
- **Grafana**: Visualization dashboards
- **ELK Stack**: Log management

## 📝 Best Practices Implemented

- **Layered Architecture**: Clear separation between ERP, Raw, Curated, and Analytics
- **Immutability**: Raw Layer is append-only, never overwritten
- **Star Schema**: Optimized dimensional model for analytics
- **Configuration Management**: Centralized settings in `config/settings.py`
- **SQL Separation**: Queries in separate `.sql` files
- **Type Safety**: Proper data types and schemas
- **Documentation**: Comprehensive docs in `docs/` directory
- **Version Control**: Git-friendly structure
- **Containerization**: Docker for reproducible environments
- **Efficient Storage**: Parquet format for columnar data
- **Performance**: DuckDB for fast analytical queries
- **Data Lineage**: Metadata tracking with timestamps
- **No ERP Analytics**: All analyses read from Curated Layer only

## 🤝 Contributing

This is a portfolio project for demonstration purposes. Feel free to fork and modify for your own use.

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Author

Data Engineer - Portfolio Project

## 📞 Contact

For questions or feedback, please open an issue in the repository.
