# Portfolio Data Engineering Project

A complete data engineering portfolio project demonstrating a full ETL pipeline with PostgreSQL, Python, Pandas, DuckDB, and Parquet for business analytics.

## 📋 Overview

This project implements a complete data pipeline that:
- Extracts data from CSV files and loads into PostgreSQL
- Transforms data using Pandas and exports to Parquet format
- Performs analytics using DuckDB on Parquet files
- Generates business metrics and insights

## 🏗️ Architecture

```
CSV (Raw Data)
    ↓
PostgreSQL (Docker)
    ↓
SQLAlchemy (Python)
    ↓
Pandas (Transform)
    ↓
Parquet Files
    ↓
DuckDB (Analytics)
    ↓
Business Metrics
```

## 🛠️ Technologies Used

- **PostgreSQL 15**: Relational database for data storage
- **Docker & Docker Compose**: Containerization and orchestration
- **Python 3.8+**: Programming language
- **SQLAlchemy**: SQL toolkit and ORM
- **Pandas**: Data manipulation and analysis
- **DuckDB**: High-performance analytical database
- **PyArrow**: Parquet file format support
- **psycopg2-binary**: PostgreSQL adapter for Python

## 📁 Project Structure

```
portfolio-data-engineering/
├── analytics/
│   ├── produto_mais_vendido.py    # Most sold product analysis
│   ├── receita_por_cliente.py    # Revenue by client analysis
│   └── receita_total.py          # Total revenue analysis
│
├── config/
│   └── settings.py               # Centralized configuration
│
├── data/
│   ├── raw/
│   │   └── vendas.csv            # Raw sales data
│   ├── processed/
│   │   ├── clientes.parquet      # Processed client data
│   │   ├── produtos.parquet      # Processed product data
│   │   └── vendas.parquet        # Processed sales data
│   └── analytics/
│       ├── receita_por_cliente.parquet
│       └── produto_mais_vendido.parquet
│
├── etl/
│   ├── extract/
│   │   └── extract_postgres.py   # Extract from CSV to PostgreSQL
│   ├── transform/
│   │   └── parquet_transform.py  # Transform PostgreSQL to Parquet
│   └── load/
│       └── load_postgres.py      # Load Parquet back to PostgreSQL
│
├── sql/
│   ├── ddl/
│   │   └── create_tables.sql     # Database schema
│   └── analytics/
│       ├── receita_total.sql
│       ├── receita_por_cliente.sql
│       └── produto_mais_vendido.sql
│
├── docker-compose.yml            # PostgreSQL container configuration
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🗄️ Data Model

### Tables

**clientes**
- `id`: Primary key
- `nome`: Customer name
- `cidade`: Customer city

**produtos**
- `id_produto`: Primary key
- `nome`: Product name
- `categoria`: Product category
- `preco`: Product price

**vendas**
- `id_venda`: Primary key
- `id_cliente`: Foreign key to clientes
- `id_produto`: Foreign key to produtos
- `quantidade`: Quantity sold
- `data_venda`: Sale date

### Relationships
- `vendas.id_cliente` → `clientes.id`
- `vendas.id_produto` → `produtos.id_produto`

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

## 🔄 Running the ETL Pipeline

### Step 1: Extract (CSV → PostgreSQL)

Load CSV data into PostgreSQL:
```bash
python etl/extract/extract_postgres.py
```

This script:
- Reads the raw CSV file from `data/raw/vendas.csv`
- Creates sample data for clientes and produtos tables
- Loads all data into PostgreSQL

### Step 2: Transform (PostgreSQL → Parquet)

Extract data from PostgreSQL and convert to Parquet:
```bash
python etl/transform/parquet_transform.py
```

This script:
- Connects to PostgreSQL using SQLAlchemy
- Extracts data from clientes, produtos, and vendas tables
- Saves each table as a Parquet file in `data/processed/`

### Step 3: Load (Optional - Parquet → PostgreSQL)

Load analytics results back to PostgreSQL:
```bash
python etl/load/load_postgres.py
```

## 📊 Running Analytics

Execute analytics scripts using DuckDB on Parquet files:

### Total Revenue
```bash
python analytics/receita_total.py
```
Calculates:
- Total revenue from all sales
- Total number of sales
- Total number of customers
- Average ticket value

### Revenue by Client
```bash
python analytics/receita_por_cliente.py
```
Calculates:
- Revenue per customer
- Total sales per customer
- Average ticket per customer
- Results sorted by revenue (descending)

### Most Sold Product
```bash
python analytics/produto_mais_vendido.py
```
Identifies:
- Product with highest quantity sold
- Total quantity sold
- Number of sales transactions
- Total revenue from this product

All analytics results are saved as Parquet files in `data/analytics/`.

## 🔧 Configuration

All configuration is centralized in `config/settings.py`:

- Database credentials
- File paths
- Directory paths
- SQL file paths

You can customize these settings without modifying the scripts.

## 📈 Business Metrics

The project calculates the following key metrics:

1. **Receita Total**: Total revenue from all sales
2. **Receita por Cliente**: Revenue breakdown by customer
3. **Produto Mais Vendido**: Best-selling product by quantity
4. **Receita por Produto**: Revenue breakdown by product
5. **Receita por Cidade**: Revenue breakdown by city
6. **Ticket Médio**: Average sale value

## 🔮 Future Enhancements

This project can be extended with:

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
- **Google Cloud Storage**: Cloud-native storage

### Visualization
- **Streamlit**: Interactive dashboards
- **Plotly Dash**: Web applications
- **Apache Superset**: Business intelligence platform

### Advanced Analytics
- **Apache Spark**: Big data processing
- **Databricks**: Unified analytics platform
- **Snowflake**: Cloud data warehouse

### Monitoring
- **Prometheus**: Metrics monitoring
- **Grafana**: Visualization dashboards
- **ELK Stack**: Log management

## 🧪 Testing

To ensure data quality and pipeline reliability:

```bash
# Run data validation (to be implemented)
python tests/test_data_quality.py

# Run ETL tests (to be implemented)
python tests/test_etl.py
```

## 📝 Best Practices Implemented

- **Modular Architecture**: Separation of concerns (extract, transform, load, analytics)
- **Configuration Management**: Centralized settings in `config/settings.py`
- **SQL Separation**: Queries in separate `.sql` files
- **Type Safety**: Proper data types and schemas
- **Documentation**: Comprehensive docstrings and comments
- **Version Control**: Git-friendly structure
- **Containerization**: Docker for reproducible environments
- **Efficient Storage**: Parquet format for columnar data
- **Performance**: DuckDB for fast analytical queries

## 🤝 Contributing

This is a portfolio project for demonstration purposes. Feel free to fork and modify for your own use.

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Author

Senior Data Engineer - Portfolio Project

## 📞 Contact

For questions or feedback, please open an issue in the repository.
