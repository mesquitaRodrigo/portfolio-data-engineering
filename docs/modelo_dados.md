# Modelo de Dados - Portfolio Data Engineering

## Visão Geral

Este documento descreve o modelo de dados utilizado no projeto, abrangendo desde o esquema operacional (ERP) até o modelo dimensional (Data Warehouse). O projeto utiliza uma abordagem de **Star Schema** para a camada curada, otimizada para consultas analíticas.

## Modelo Operacional (ERP - PostgreSQL)

O ERP utiliza um modelo relacional normalizado (3NF) focado em integridade transacional.

### Tabela: clientes
Armazena informações dos clientes do sistema.

| Coluna | Tipo | Descrição | Chave |
|--------|------|-----------|-------|
| id | SERIAL | Identificador único do cliente | PK |
| nome | VARCHAR(100) | Nome completo do cliente | - |
| cidade | VARCHAR(100) | Cidade do cliente | - |
| email | VARCHAR(100) | Email do cliente | - |
| telefone | VARCHAR(20) | Telefone do cliente | - |
| data_cadastro | DATE | Data de cadastro do cliente | - |
| ativo | BOOLEAN | Status do cliente (ativo/inativo) | - |

**Índices:**
- idx_clientes_cidade (cidade)
- idx_clientes_ativo (ativo)

### Tabela: produtos
Armazena informações dos produtos disponíveis para venda.

| Coluna | Tipo | Descrição | Chave |
|--------|------|-----------|-------|
| id_produto | SERIAL | Identificador único do produto | PK |
| nome | VARCHAR(100) | Nome do produto | - |
| categoria | VARCHAR(50) | Categoria do produto | - |
| preco | DECIMAL(10,2) | Preço unitário do produto | - |
| estoque | INTEGER | Quantidade em estoque | - |
| data_cadastro | DATE | Data de cadastro do produto | - |
| ativo | BOOLEAN | Status do produto (ativo/inativo) | - |

**Índices:**
- idx_produtos_categoria (categoria)
- idx_produtos_ativo (ativo)

### Tabela: pedidos
Armazena informações dos pedidos realizados pelos clientes.

| Coluna | Tipo | Descrição | Chave |
|--------|------|-----------|-------|
| id_pedido | SERIAL | Identificador único do pedido | PK |
| id_cliente | INTEGER | Identificador do cliente | FK |
| data_pedido | DATE | Data do pedido | - |
| status | VARCHAR(20) | Status do pedido | - |
| valor_total | DECIMAL(10,2) | Valor total do pedido | - |

**Índices:**
- idx_pedidos_id_cliente (id_cliente)
- idx_pedidos_data_pedido (data_pedido)
- idx_pedidos_status (status)

**Relacionamentos:**
- id_cliente → clientes(id)

### Tabela: itens_pedido
Armazena os itens individuais de cada pedido.

| Coluna | Tipo | Descrição | Chave |
|--------|------|-----------|-------|
| id_item | SERIAL | Identificador único do item | PK |
| id_pedido | INTEGER | Identificador do pedido | FK |
| id_produto | INTEGER | Identificador do produto | FK |
| quantidade | INTEGER | Quantidade do produto | - |
| preco_unitario | DECIMAL(10,2) | Preço unitário na venda | - |
| subtotal | DECIMAL(10,2) | Subtotal (quantidade * preco_unitario) | GENERATED |

**Índices:**
- idx_itens_pedido_id_pedido (id_pedido)
- idx_itens_pedido_id_produto (id_produto)

**Relacionamentos:**
- id_pedido → pedidos(id_pedido)
- id_produto → produtos(id_produto)

## Modelo Dimensional (Curated Layer - Star Schema)

A camada curada utiliza um modelo estrela (Star Schema) otimizado para consultas analíticas.

### Dimensão: dim_cliente
Dimensão que descreve os clientes do sistema.

| Coluna | Tipo | Descrição | Origem |
|--------|------|-----------|--------|
| sk_cliente | INTEGER | Surrogate Key (chave substituta) | Gerada |
| nk_cliente | INTEGER | Natural Key (chave natural) | clientes.id |
| nome | VARCHAR(100) | Nome completo do cliente | clientes.nome |
| cidade | VARCHAR(100) | Cidade do cliente | clientes.cidade |
| email | VARCHAR(100) | Email do cliente | clientes.email |
| telefone | VARCHAR(20) | Telefone do cliente | clientes.telefone |
| data_cadastro | DATE | Data de cadastro | clientes.data_cadastro |
| ativo | BOOLEAN | Status do cliente | clientes.ativo |
| extract_timestamp | TIMESTAMP | Timestamp da extração | Gerada |
| dw_load_timestamp | TIMESTAMP | Timestamp da carga no DW | Gerada |

**Características:**
- sk_cliente: Chave surrogate interna do DW
- nk_cliente: Chave natural do sistema fonte
- Metadados de linhagem (extract_timestamp, dw_load_timestamp)

### Dimensão: dim_produto
Dimensão que descreve os produtos disponíveis.

| Coluna | Tipo | Descrição | Origem |
|--------|------|-----------|--------|
| sk_produto | INTEGER | Surrogate Key (chave substituta) | Gerada |
| nk_produto | INTEGER | Natural Key (chave natural) | produtos.id_produto |
| nome | VARCHAR(100) | Nome do produto | produtos.nome |
| categoria | VARCHAR(50) | Categoria do produto | produtos.categoria |
| preco | DECIMAL(10,2) | Preço unitário atual | produtos.preco |
| estoque | INTEGER | Quantidade em estoque | produtos.estoque |
| data_cadastro | DATE | Data de cadastro | produtos.data_cadastro |
| ativo | BOOLEAN | Status do produto | produtos.ativo |
| extract_timestamp | TIMESTAMP | Timestamp da extração | Gerada |
| dw_load_timestamp | TIMESTAMP | Timestamp da carga no DW | Gerada |

**Características:**
- sk_produto: Chave surrogate interna do DW
- nk_produto: Chave natural do sistema fonte
- Metadados de linhagem (extract_timestamp, dw_load_timestamp)

### Fato: fato_vendas
Tabela fato que armazena as transações de vendas.

| Coluna | Tipo | Descrição | Origem |
|--------|------|-----------|--------|
| sk_venda | INTEGER | Surrogate Key da venda | Gerada |
| nk_pedido | INTEGER | Natural Key do pedido | itens_pedido.id_pedido |
| sk_produto | INTEGER | Foreign Key para dim_produto | dim_produto.sk_produto |
| sk_cliente | INTEGER | Foreign Key para dim_cliente | dim_cliente.sk_cliente |
| quantidade | INTEGER | Quantidade vendida | itens_pedido.quantidade |
| preco_unitario | DECIMAL(10,2) | Preço unitário na venda | itens_pedido.preco_unitario |
| valor_total | DECIMAL(10,2) | Valor total da venda | itens_pedido.subtotal |
| data_venda | DATE | Data da venda | pedidos.data_pedido |
| status | VARCHAR(20) | Status do pedido | pedidos.status |
| extract_timestamp | TIMESTAMP | Timestamp da extração | Gerada |
| dw_load_timestamp | TIMESTAMP | Timestamp da carga no DW | Gerada |

**Características:**
- sk_venda: Chave surrogate única para cada item vendido
- nk_pedido: Chave natural do pedido (para rastreabilidade)
- sk_produto: Foreign Key para dim_produto
- sk_cliente: Foreign Key para dim_cliente
- Métricas: quantidade, preco_unitario, valor_total
- Dimensões: data_venda, status

## Diagrama do Modelo Dimensional

```
                    ┌──────────────────┐
                    │   dim_cliente    │
                    ├──────────────────┤
                    │ sk_cliente (PK)  │
                    │ nk_cliente       │
                    │ nome             │
                    │ cidade           │
                    │ email            │
                    │ telefone         │
                    │ data_cadastro    │
                    │ ativo            │
                    │ extract_ts       │
                    │ dw_load_ts       │
                    └────────┬─────────┘
                             │
                             │ 1
                             │
                             │ N
                             │
                    ┌────────▼─────────┐
                    │  fato_vendas     │
                    ├──────────────────┤
                    │ sk_venda (PK)    │
                    │ nk_pedido        │
                    │ sk_produto (FK)  │◄─────────┐
                    │ sk_cliente (FK)  │          │
                    │ quantidade       │          │
                    │ preco_unitario   │          │
                    │ valor_total      │          │
                    │ data_venda       │          │
                    │ status           │          │
                    │ extract_ts       │          │
                    │ dw_load_ts       │          │
                    └──────────────────┘          │
                             │                    │
                             │ N                  │ 1
                             │                    │
                    ┌────────▼─────────┐    ┌─────┴──────────┐
                    │  dim_produto     │    │  dim_tempo    │
                    ├──────────────────┤    ├───────────────┤
                    │ sk_produto (PK)  │    │ sk_tempo (PK) │
                    │ nk_produto       │    │ data_venda    │
                    │ nome             │    │ ano           │
                    │ categoria        │    │ mes           │
                    │ preco            │    │ dia           │
                    │ estoque          │    │ trimestre     │
                    │ data_cadastro    │    │ dia_semana    │
                    │ ativo            │    │ fim_semana    │
                    │ extract_ts       │    └───────────────┘
                    │ dw_load_ts       │
                    └──────────────────┘
```

**Nota:** A dimensão tempo (dim_tempo) pode ser adicionada futuramente para análises temporais mais detalhadas.

## Mapeamento ERP → Data Warehouse

### clientes → dim_cliente
```
ERP (clientes)          →  DW (dim_cliente)
id                      →  nk_cliente, sk_cliente
nome                    →  nome
cidade                  →  cidade
email                   →  email
telefone                →  telefone
data_cadastro           →  data_cadastro
ativo                   →  ativo
(NOW)                   →  extract_timestamp
(NOW)                   →  dw_load_timestamp
```

### produtos → dim_produto
```
ERP (produtos)          →  DW (dim_produto)
id_produto              →  nk_produto, sk_produto
nome                    →  nome
categoria               →  categoria
preco                   →  preco
estoque                 →  estoque
data_cadastro           →  data_cadastro
ativo                   →  ativo
(NOW)                   →  extract_timestamp
(NOW)                   →  dw_load_timestamp
```

### pedidos + itens_pedido → fato_vendas
```
ERP (itens_pedido)      →  DW (fato_vendas)
id_item                 →  sk_venda
id_pedido               →  nk_pedido
id_produto              →  sk_produto (via dim_produto)
quantidade              →  quantidade
preco_unitario          →  preco_unitario
subtotal                →  valor_total

ERP (pedidos)           →  DW (fato_vendas)
id_cliente              →  sk_cliente (via dim_cliente)
data_pedido             →  data_venda
status                  →  status

(Gerado)                →  extract_timestamp
(Gerado)                →  dw_load_timestamp
```

## Métricas e KPIs

### Métricas Disponíveis
1. **Receita Total**: Soma de valor_total em fato_vendas
2. **Receita por Cliente**: Soma de valor_total agrupado por sk_cliente
3. **Receita por Produto**: Soma de valor_total agrupado por sk_produto
4. **Receita por Cidade**: Soma de valor_total agrupado por cidade (via dim_cliente)
5. **Ticket Médio**: Média de valor_total por venda
6. **Produto Mais Vendido**: Produto com maior quantidade vendida

### KPIs Sugeridos
- **CAGR (Compound Annual Growth Rate)**: Crescimento da receita ao longo do tempo
- **CLV (Customer Lifetime Value)**: Valor total por cliente ao longo do tempo
- **Churn Rate**: Taxa de perda de clientes
- **Average Order Value (AOV)**: Ticket médio
- **Repeat Purchase Rate**: Taxa de compras recorrentes
- **Product Mix**: Distribuição de vendas por categoria

## Regras de Negócio

### Validação de Dados
1. **Clientes**: Apenas clientes ativos (ativo = TRUE)
2. **Produtos**: Apenas produtos ativos (ativo = TRUE)
3. **Pedidos**: Apenas pedidos com status concluído/enviado/entregue
4. **Vendas**: Valor total deve ser positivo
5. **Quantidade**: Quantidade deve ser maior que zero

### Transformações
1. **Chaves Surrogate**: Geradas automaticamente no DW
2. **Timestamps**: Adicionados em cada etapa (extract, load)
3. **Status**: Filtragem de pedidos não concluídos
4. **Cálculos**: subtotal = quantidade * preco_unitario

### Linhagem de Dados
- **extract_timestamp**: Quando o dado foi extraído do ERP
- **dw_load_timestamp**: Quando o dado foi carregado no DW
- **nk_***: Chaves naturais para rastreabilidade
- **sk_***: Chaves surrogate para performance

## Performance e Otimização

### Índices Sugeridos (Curated Layer)
```sql
-- dim_cliente
CREATE INDEX idx_dim_cliente_sk_cliente ON dim_cliente(sk_cliente);
CREATE INDEX idx_dim_cliente_cidade ON dim_cliente(cidade);

-- dim_produto
CREATE INDEX idx_dim_produto_sk_produto ON dim_produto(sk_produto);
CREATE INDEX idx_dim_produto_categoria ON dim_produto(categoria);

-- fato_vendas
CREATE INDEX idx_fato_vendas_sk_venda ON fato_vendas(sk_venda);
CREATE INDEX idx_fato_vendas_sk_produto ON fato_vendas(sk_produto);
CREATE INDEX idx_fato_vendas_sk_cliente ON fato_vendas(sk_cliente);
CREATE INDEX idx_fato_vendas_data_venda ON fato_vendas(data_venda);
```

### Particionamento (Futuro)
- **Por Data**: Particionar fato_vendas por data_venda (mensal/anual)
- **Por Região**: Particionar dim_cliente por região geográfica
- **Por Categoria**: Particionar dim_produto por categoria

### Compressão
- **Parquet**: Compressão automática columnar
- **Encoding**: Snappy ou ZSTD para melhor compressão
- **Statistics**: Estatísticas coletadas automaticamente

## Evolução do Modelo

### Fase 1 (Atual)
- Modelo estrela básico
- 2 dimensões (cliente, produto)
- 1 fato (vendas)
- Analytics básicos

### Fase 2 (Curto Prazo)
- Adicionar dimensão tempo (dim_tempo)
- Adicionar dimensão categoria (dim_categoria)
- Enriquecer fato_vendas com mais métricas
- Implementar SCD (Slowly Changing Dimensions) Tipo 2

### Fase 3 (Médio Prazo)
- Adicionar fato_orcamento (budget vs actual)
- Adicionar fato_estoque (inventory)
- Adicionar fato_marketing (campaign performance)
- Implementar hierarquias nas dimensões

### Fase 4 (Longo Prazo)
- Modelo snowflake para maior granularidade
- Dimensões conformadas (conformed dimensions)
- Múltiplos fatos compartilhando dimensões
- Data vault para linhagem avançada

## Dicionário de Dados

### Abreviações
- **sk_**: Surrogate Key (chave substituta)
- **nk_**: Natural Key (chave natural)
- **pk**: Primary Key (chave primária)
- **fk**: Foreign Key (chave estrangeira)
- **ts**: Timestamp

### Convenções de Nomenclatura
- **Tabelas**: snake_case (ex: dim_cliente, fato_vendas)
- **Colunas**: snake_case (ex: sk_cliente, valor_total)
- **Prefixos**: sk_, nk_ para chaves
- **Sufixos**: _timestamp para datas/horas

### Tipos de Dados
- **INTEGER**: Números inteiros
- **VARCHAR**: Texto de comprimento variável
- **DECIMAL**: Números decimais (precisão fixa)
- **DATE**: Data (ano, mês, dia)
- **TIMESTAMP**: Data e hora
- **BOOLEAN**: Verdadeiro/Falso

## Qualidade de Dados

### Validações Implementadas
1. **Integridade Referencial**: Foreign keys válidas
2. **Não Nulidade**: Campos obrigatórios preenchidos
3. **Domínio**: Valores dentro de faixas aceitáveis
4. **Unicidade**: Chaves primárias únicas
5. **Consistência**: Relacionamentos lógicos

### Validações Futuras
1. **Great Expectations**: Testes automatizados de qualidade
2. **Pandera**: Validação de schemas em Python
3. **dbt Tests**: Testes de dados em transformações
4. **Data Quality Dashboards**: Monitoramento contínuo

## Governança de Dados

### Proprietários de Dados
- **clientes**: Equipe de CRM/Vendas
- **produtos**: Equipe de Produto/Estoque
- **pedidos**: Equipe de Operações
- **itens_pedido**: Equipe de Operações

### SLA (Service Level Agreement)
- **Freshness**: Dados atualizados até 24h após o evento
- **Availability**: 99.9% uptime do DW
- **Accuracy**: 99.5% precisão dos dados
- **Completeness**: 100% dos registros processados

### Retenção de Dados
- **Raw Layer**: Retenção permanente (append-only)
- **Curated Layer**: Retenção de 7 anos
- **Analytics Layer**: Retenção de 1 ano
- **Logs**: Retenção de 90 dias
