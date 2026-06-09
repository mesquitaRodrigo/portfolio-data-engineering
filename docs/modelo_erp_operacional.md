# Modelo ERP Operacional - Diagrama Textual

## Diagrama de Relacionamentos (ASCII)

```
┌─────────────────────────────────────────────────────────────────┐
│                        ERP (PostgreSQL)                         │
│                    Sistema Operacional (OLTP)                   │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│    clientes      │
├──────────────────┤
│ id_cliente (PK)  │
│ nome             │
│ cidade           │
└────────┬─────────┘
         │ 1
         │
         │ N
┌────────▼─────────┐
│    pedidos       │
├──────────────────┤
│ id_pedido (PK)   │
│ id_cliente (FK)  │
│ data_pedido      │
└────────┬─────────┘
         │ 1
         │
         │ N
┌────────▼─────────┐         ┌──────────────────┐
│   itens_pedido   │────────▶│    produtos      │
├──────────────────┤  N      ├──────────────────┤
│ id_item (PK)     │◀────────│ id_produto (PK)  │
│ id_pedido (FK)   │    1    │ nome             │
│ id_produto (FK)  │         │ categoria        │
│ quantidade       │         │ preco            │
│ preco_unitario   │         └──────────────────┘
└──────────────────┘
```

## Relacionamentos

### clientes (1:N) pedidos
- Um cliente pode ter múltiplos pedidos
- Cada pedido pertence a exatamente um cliente
- Foreign Key: `pedidos.id_cliente → clientes.id_cliente`

### pedidos (1:N) itens_pedido
- Um pedido pode ter múltiplos itens
- Cada item pertence a exatamente um pedido
- Foreign Key: `itens_pedido.id_pedido → pedidos.id_pedido`

### produtos (1:N) itens_pedido
- Um produto pode estar em múltiplos itens de pedido
- Cada item refere-se a exatamente um produto
- Foreign Key: `itens_pedido.id_produto → produtos.id_produto`

## Estrutura das Tabelas

### clientes
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id_cliente | SERIAL (PK) | Identificador único do cliente |
| nome | VARCHAR(100) | Nome completo do cliente |
| cidade | VARCHAR(100) | Cidade do cliente |

### produtos
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id_produto | SERIAL (PK) | Identificador único do produto |
| nome | VARCHAR(100) | Nome do produto |
| categoria | VARCHAR(50) | Categoria do produto |
| preco | DECIMAL(10,2) | Preço unitário do produto |

### pedidos
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id_pedido | SERIAL (PK) | Identificador único do pedido |
| id_cliente | INTEGER (FK) | Identificador do cliente |
| data_pedido | DATE | Data do pedido |

### itens_pedido
| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id_item | SERIAL (PK) | Identificador único do item |
| id_pedido | INTEGER (FK) | Identificador do pedido |
| id_produto | INTEGER (FK) | Identificador do produto |
| quantidade | INTEGER | Quantidade de itens |
| preco_unitario | DECIMAL(10,2) | Preço unitário na data da venda |

## Índices Recomendados

### Performance de Joins
- `idx_pedidos_id_cliente` em `pedidos(id_cliente)`
- `idx_itens_pedido_id_pedido` em `itens_pedido(id_pedido)`
- `idx_itens_pedido_id_produto` em `itens_pedido(id_produto)`

### Performance de Consultas Analíticas
- `idx_pedidos_data_pedido` em `pedidos(data_pedido)`
- `idx_itens_pedido_pedido_produto` em `itens_pedido(id_pedido, id_produto)`
- `idx_clientes_cidade` em `clientes(cidade)`
- `idx_produtos_categoria` em `produtos(categoria)`

## Restrições de Integridade

### Foreign Keys
- `pedidos.id_cliente` → `clientes.id_cliente` (ON DELETE RESTRICT, ON UPDATE CASCADE)
- `itens_pedido.id_pedido` → `pedidos.id_pedido` (ON DELETE CASCADE, ON UPDATE CASCADE)
- `itens_pedido.id_produto` → `produtos.id_produto` (ON DELETE RESTRICT, ON UPDATE CASCADE)

### Check Constraints
- `clientes.nome`: não pode ser vazio
- `clientes.cidade`: não pode ser vazio
- `produtos.nome`: não pode ser vazio
- `produtos.categoria`: não pode ser vazio
- `produtos.preco`: deve ser maior que 0
- `pedidos.data_pedido`: não pode ser futura
- `itens_pedido.quantidade`: deve ser maior que 0
- `itens_pedido.preco_unitario`: deve ser maior que 0

## Características do Modelo

### Normalização
- **3NF (Third Normal Form)**: O modelo está na terceira forma normal
- Sem redundância de dados
- Dependências funcionais bem definidas
- Integridade referencial garantida

### Transacionalidade
- **OLTP (Online Transaction Processing)**: Otimizado para transações
- Alta frequência de escrita
- Integridade ACID garantida pelo PostgreSQL
- Locks granulares para concorrência

### Escalabilidade
- Preparado para crescimento de volume
- Índices otimizados para consultas comuns
- Estrutura relacional bem definida
- Suporte a particionamento futuro
