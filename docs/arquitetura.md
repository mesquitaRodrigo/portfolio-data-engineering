# Arquitetura do Projeto de Engenharia de Dados

## Visão Geral

Este projeto implementa uma arquitetura em camadas inspirada em Data Lake + Data Warehouse, seguindo as melhores práticas de engenharia de dados modernas. A arquitetura separa claramente as responsabilidades entre o sistema operacional (ERP), armazenamento de dados brutos (Raw Layer), dados curados (Curated Layer), e análise de dados (Analytics).

## Fluxo de Dados

```
┌─────────────────────────────────────────────────────────────────┐
│                         ERP (PostgreSQL)                         │
│                    Sistema Operacional                          │
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
│                  Banco de Dados Analítico                       │
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

## Camadas da Arquitetura

### 1. ERP (PostgreSQL) - Sistema Operacional
- **Propósito**: Sistema transacional original (OLTP)
- **Tecnologia**: PostgreSQL 15
- **Tabelas**: clientes, produtos, pedidos, itens_pedido
- **Características**:
  - Dados normalizados (3NF)
  - Foco em integridade e consistência
  - Alta frequência de escrita
  - Não utilizado para análise direta

### 2. Raw Layer - Camada Bruta (Data Lake)
- **Propósito**: Armazenamento de dados extraídos sem transformação
- **Tecnologia**: Arquivos Parquet
- **Localização**: `data/raw/`
- **Arquivos**:
  - clientes.parquet
  - produtos.parquet
  - pedidos.parquet
  - itens_pedido.parquet
- **Características**:
  - Dados brutos, extraídos diretamente do ERP
  - Preservação do estado original
  - Imutável (append-only)
  - Alta compressão (Parquet)
  - Pronto para processamento distribuído

### 3. Curated Layer - Camada Curada (Data Warehouse)
- **Propósito**: Modelo dimensional para análise (OLAP)
- **Tecnologia**: Arquivos Parquet
- **Localização**: `data/curated/`
- **Tabelas**:
  - dim_cliente.parquet (Dimensão Cliente)
  - dim_produto.parquet (Dimensão Produto)
  - fato_vendas.parquet (Fato Vendas)
- **Características**:
  - Modelo estrela (Star Schema)
  - Dados limpos e transformados
  - Chaves surrogate (sk_) e natural (nk_)
  - Metadados de carga (dw_load_timestamp)
  - Otimizado para consultas analíticas

### 4. DuckDB - Motor Analítico
- **Propósito**: Execução de consultas analíticas de alta performance
- **Tecnologia**: DuckDB
- **Características**:
  - Processamento em memória
  - Compatibilidade com SQL ANSI
  - Leitura direta de arquivos Parquet
  - Columnar storage
  - Zero overhead de deployment

### 5. Analytics Layer - Camada de Análises
- **Propósito**: Armazenamento de resultados de métricas de negócio
- **Tecnologia**: Arquivos Parquet
- **Localização**: `data/analytics/`
- **Métricas**:
  - receita_total.parquet
  - receita_por_cliente.parquet
  - receita_por_produto.parquet
  - receita_por_cidade.parquet
  - ticket_medio.parquet
  - produto_mais_vendido.parquet
- **Características**:
  - Resultados pré-calculados
  - Prontos para visualização
  - Cache de consultas complexas

## Componentes ETL

### Extract (Extração)
- **Localização**: `etl/extract/`
- **Scripts**:
  - extract_clientes.py
  - extract_produtos.py
  - extract_pedidos.py
  - extract_itens_pedido.py
- **SQL**: `sql/extract/`
- **Função**: Extrair dados do ERP para Raw Layer
- **Frequência**: Batch (pode ser agendado)

### Transform (Transformação)
- **Localização**: `etl/transform/`
- **Scripts**:
  - criar_dim_cliente.py
  - criar_dim_produto.py
  - criar_fato_vendas.py
- **SQL**: `sql/transform/`
- **Função**: Transformar dados brutos em modelo dimensional
- **Lógica**:
  - Limpeza de dados
  - Criação de chaves surrogate
  - Enriquecimento de dados
  - Adição de metadados

### Load (Carga)
- **Localização**: `etl/load/`
- **Scripts**:
  - load_duckdb.py
- **Função**: Carregar dados do Curated Layer para DuckDB
- **Características**:
  - Criação de views no DuckDB
  - Validação de dados
  - Preparação para analytics

## Analytics (Análises)
- **Localização**: `analytics/`
- **Scripts**:
  - receita_total.py
  - receita_por_cliente.py
  - receita_por_produto.py
  - receita_por_cidade.py
  - ticket_medio.py
  - produto_mais_vendido.py
- **SQL**: `sql/analytics/`
- **Função**: Executar consultas analíticas no Curated Layer
- **Saída**: Arquivos Parquet com resultados

## Princípios da Arquitetura

### 1. Separação de Responsabilidades
- ERP: Sistema operacional (OLTP)
- Data Lake: Armazenamento bruto
- Data Warehouse: Dados curados para análise
- Analytics: Métricas de negócio

### 2. Imutabilidade
- Raw Layer: Append-only, nunca sobrescrito
- Curated Layer: Recarga completa ou incremental
- Analytics: Regenerado sob demanda

### 3. Performance
- Parquet: Compressão columnar eficiente
- DuckDB: Processamento em memória
- Star Schema: Otimizado para consultas analíticas

### 4. Escalabilidade
- Arquivos: Processamento distribuído possível
- Cloud-ready: Preparado para S3, Azure Data Lake
- Orquestração: Preparado para Airflow

### 5. Governança de Dados
- Linhagem: Rastreabilidade completa
- Metadados: Timestamps de extração e carga
- Qualidade: Validação em cada camada

## Integrações Futuras

### Orquestração
- **Apache Airflow**: Agendamento e monitoramento de pipelines
- **dbt**: Transformações como código
- **Prefect**: Orquestração moderna

### Armazenamento em Nuvem
- **AWS S3**: Armazenamento de objetos escalável
- **Azure Data Lake**: Data lake enterprise
- **MinIO**: S3-compatible local

### Visualização
- **Power BI**: Business intelligence
- **Streamlit**: Dashboards interativos
- **Apache Superset**: BI open-source

### Processamento Distribuído
- **Apache Spark**: Big data processing
- **Databricks**: Plataforma unificada
- **Snowflake**: Cloud data warehouse

## Benefícios da Arquitetura

### 1. Desacoplamento
- ERP isolado de cargas analíticas
- Mudanças no ERP não afetam analytics
- Independência entre camadas

### 2. Performance
- Consultas analíticas não impactam ERP
- DuckDB para queries rápidas
- Parquet para armazenamento eficiente

### 3. Flexibilidade
- Fácil adicionar novas métricas
- Suporte a múltiplas fontes de dados
- Extensível para novos casos de uso

### 4. Confiabilidade
- Dados brutos preservados
- Rastreabilidade completa
- Recuperação de desastres facilitada

### 5. Manutenibilidade
- Código modular e reutilizável
- SQL separado em arquivos
- Configuração centralizada

## Monitoramento e Observabilidade

### Métricas a Implementar
- Tempo de execução de cada etapa ETL
- Volume de dados processado
- Taxa de sucesso/falha
- Latência de dados (data freshness)
- Qualidade de dados (data quality)

### Logs
- Logs estruturados em JSON
- Níveis de log apropriados
- Armazenamento centralizado (ELK Stack)

### Alertas
- Falhas no pipeline ETL
- Anomalias nos dados
- Performance degradation
- Problemas de conectividade

## Segurança

### Autenticação
- Credenciais em variáveis de ambiente
- Secrets management (HashiCorp Vault)
- Role-based access control

### Autorização
- Permissões por camada
- Acesso granular a tabelas
- Auditoria de acessos

### Criptografia
- Dados em trânsito (TLS)
- Dados em repouso (encryption at rest)
- Chaves gerenciadas adequadamente

## Backup e Recovery

### Estratégia de Backup
- Backup do ERP (PostgreSQL)
- Backup do Raw Layer (Parquet files)
- Backup do Curated Layer
- Backup de configurações

### Recovery
- RPO (Recovery Point Objective): Definido
- RTO (Recovery Time Objective): Definido
- Procedimentos documentados
- Testes regulares de disaster recovery
