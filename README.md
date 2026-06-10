# Portfolio Data Engineering

Pipeline completa de Engenharia de Dados desenvolvida com PostgreSQL, Python, Parquet, Docker e Metabase.

O projeto simula um ambiente corporativo com uma arquitetura moderna de dados, incluindo:

* ERP Operacional (PostgreSQL)
* Raw Layer (Data Lake)
* Curated Layer (Modelo Dimensional)
* Analytics Layer (Métricas de Negócio)
* Data Quality
* Testes Automatizados
* Dashboard no Metabase

---

## Arquitetura

```text
                 ERP OPERACIONAL
                   PostgreSQL
                        |
                        v
+------------------------------------------------+
|                  RAW LAYER                     |
|              Arquivos Parquet                  |
+------------------------------------------------+
                        |
                        v
+------------------------------------------------+
|                CURATED LAYER                   |
|             Modelo Dimensional                 |
|                                                |
|  dim_cliente                                   |
|  dim_produto                                   |
|  dim_data                                      |
|  fato_vendas                                   |
+------------------------------------------------+
                        |
                        v
+------------------------------------------------+
|               ANALYTICS LAYER                  |
|                                                |
| Receita Total                                  |
| Receita por Cliente                            |
| Receita por Produto                            |
| Receita por Cidade                             |
| Ticket Médio                                   |
| Produto Mais Vendido                           |
| Top Clientes                                   |
| Top Produtos                                   |
| Receita Mensal                                 |
+------------------------------------------------+
                        |
                        v
+------------------------------------------------+
|                  METABASE                      |
|             Dashboards e KPIs                  |
+------------------------------------------------+
```

---

## Tecnologias Utilizadas

* Python 3
* PostgreSQL
* Pandas
* PyArrow
* SQLAlchemy
* Docker
* Docker Compose
* Metabase
* Parquet

---

## Modelo Operacional (ERP)

### clientes

| Campo      | Tipo    |
| ---------- | ------- |
| id_cliente | INT     |
| nome       | VARCHAR |
| cidade     | VARCHAR |

### produtos

| Campo      | Tipo    |
| ---------- | ------- |
| id_produto | INT     |
| nome       | VARCHAR |
| categoria  | VARCHAR |
| preco      | NUMERIC |

### pedidos

| Campo       | Tipo |
| ----------- | ---- |
| id_pedido   | INT  |
| id_cliente  | INT  |
| data_pedido | DATE |

### itens_pedido

| Campo          | Tipo    |
| -------------- | ------- |
| id_item        | INT     |
| id_pedido      | INT     |
| id_produto     | INT     |
| quantidade     | INT     |
| preco_unitario | NUMERIC |

---

## Estrutura do Projeto

```text
portfolio-data-engineering/

├── analytics/
│   └── run_analytics.py
│
├── config/
│   └── settings.py
│
├── data/
│   ├── raw/
│   ├── curated/
│   └── analytics/
│
├── docs/
│
├── etl/
│   ├── extract/
│   ├── transform/
│   ├── load/
│   └── quality/
│
├── sql/
│
├── tests/
│
├── run_pipeline.py
├── test_project.py
└── README.md
```

---

## Camadas do Pipeline

### 1. ERP Layer

Fonte operacional dos dados.

Tabelas:

* clientes
* produtos
* pedidos
* itens_pedido

---

### 2. Raw Layer

Extração direta do ERP para arquivos Parquet.

Arquivos:

* clientes.parquet
* produtos.parquet
* pedidos.parquet
* itens_pedido.parquet

---

### 3. Curated Layer

Modelo dimensional criado para análises.

Dimensões:

* dim_cliente
* dim_produto
* dim_data

Fato:

* fato_vendas

---

### 4. Analytics Layer

Métricas consolidadas para consumo analítico.

Tabelas:

* receita_total
* receita_por_cliente
* receita_por_produto
* receita_por_cidade
* ticket_medio
* produto_mais_vendido
* top_clientes
* top_produtos
* receita_mensal

---

## Data Quality

Validações implementadas:

### Raw Layer

* Campos obrigatórios
* Valores nulos
* Valores negativos
* Integridade básica

### Curated Layer

* Integridade dimensional
* Validação da fato
* Chaves obrigatórias

### Regras de Negócio

* Todo pedido possui itens
* Todo item possui produto válido
* Todo pedido possui cliente válido

Resultado:

```text
Total de Validações: 29
Validações Aprovadas: 29
Taxa de Sucesso: 100%
```

---

## Testes Automatizados

Cobertura atual:

```text
Total de Testes: 69
Testes Aprovados: 69
Taxa de Sucesso: 100%
```

Validações:

* Conexão PostgreSQL
* Estrutura ERP
* Dados ERP
* Integridade Referencial
* Raw Layer
* Curated Layer
* Analytics Layer
* Schemas
* Contagem de Registros

---

## Executando o Projeto

### Clonar

```bash
git clone https://github.com/mesquitaRodrigo/portfolio-data-engineering.git

cd portfolio-data-engineering
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Executar pipeline

```bash
python3 run_pipeline.py
```

### Executar testes

```bash
python3 test_project.py
```

### Executar Data Quality

```bash
python3 etl/quality/data_quality.py
```

---

## Dashboard Metabase

KPIs implementados:

### Receita Total

```text
R$ 49.070
```

### Ticket Médio

```text
R$ 2.453,50
```

Além de:

* Receita por Cliente
* Receita por Cidade
* Receita Mensal
* Produtos Mais Vendidos
* Top Clientes
* Top Produtos

---

## Resultados

### Dados Operacionais

| Entidade     | Registros |
| ------------ | --------- |
| Clientes     | 10        |
| Produtos     | 10        |
| Pedidos      | 20        |
| Itens Pedido | 46        |

### Modelo Dimensional

| Tabela      | Registros |
| ----------- | --------- |
| dim_cliente | 10        |
| dim_produto | 10        |
| dim_data    | 20        |
| fato_vendas | 46        |

---

## Próximos Passos

* Orquestração com Apache Airflow
* Data Warehouse incremental
* Particionamento de dados
* Docker Compose completo
* CI/CD com GitHub Actions
* Deploy em ambiente cloud
* Monitoramento de pipelines

---

## Autor

Rodrigo Mesquita

Projeto desenvolvido para demonstrar competências em:

* Engenharia de Dados
* Modelagem Dimensional
* ETL
* Data Quality
* Analytics Engineering
* PostgreSQL
* Python
* Docker
* Metabase
