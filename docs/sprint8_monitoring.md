# Sprint 8 - Observabilidade, Monitoramento e Logging

## Overview

Sprint 8 implementa observabilidade, monitoramento e logging centralizado para o projeto portfolio-data-engineering. Esta sprint adiciona capacidades de rastreamento de execuções, métricas de qualidade de dados, auditoria em PostgreSQL e dashboards de monitoramento.

## Arquitetura

### Componentes Implementados

1. **Logging Centralizado**
   - Estrutura de logs estruturados
   - Formato padronizado: `YYYY-MM-DD HH:MM:SS | LEVEL | PROCESS | Message`
   - Logs separados por componente: pipeline, quality, analytics, airflow

2. **Monitoramento de Execuções**
   - Rastreamento de início/fim de execuções
   - Cálculo de duração
   - Registro de status (success, failed, partial)
   - Contagem de registros processados
   - Persistência em CSV e PostgreSQL

3. **Métricas de Qualidade de Dados**
   - Cálculo automático de métricas de qualidade
   - Percentual de nulos
   - Percentual de duplicados
   - Percentual de integridade
   - Armazenamento em Parquet

4. **Auditoria PostgreSQL**
   - Schema `audit` com tabela `pipeline_execution`
   - Registro histórico de todas as execuções
   - Índices para consultas otimizadas
   - Trigger para atualização automática de timestamps

5. **Integração Airflow**
   - Task `monitor_task` adicionada ao DAG
   - Geração de métricas de qualidade após validação
   - Fluxo atualizado: extract >> curated >> analytics >> quality >> monitor >> tests

## Estrutura de Diretórios

```
portfolio-data-engineering/
├── config/
│   └── logging_config.py          # Configuração de logging estruturado
├── logs/
│   ├── pipeline.log                # Logs de execução da pipeline
│   ├── quality.log                 # Logs de validação de qualidade
│   ├── analytics.log               # Logs de analytics
│   └── airflow.log                 # Logs do Airflow
├── monitoring/
│   ├── pipeline_monitor.py         # Módulo de monitoramento
│   └── execution_history.csv       # Histórico de execuções (CSV)
├── sql/
│   └── audit/
│       └── create_audit_schema.sql  # Script de criação do schema audit
├── analytics/
│   └── generate_data_quality_metrics.py  # Gerador de métricas de qualidade
├── airflow/
│   └── dags/
│       └── portfolio_pipeline.py   # DAG atualizada com monitor_task
├── docs/
│   ├── observability_dashboard.md  # Documentação do dashboard
│   └── sprint8_monitoring.md        # Este documento
├── run_pipeline.py                 # Pipeline atualizada com monitoramento
└── test_project.py                 # Testes atualizados com validações
```

## Fluxo de Monitoramento

### 1. Inicialização

```python
from monitoring.pipeline_monitor import PipelineMonitor

monitor = PipelineMonitor()
monitor.start_execution('extract')
```

### 2. Execução

A pipeline executa normalmente com logging estruturado:

```
2026-06-10 10:30:00 | INFO | PIPELINE | Iniciando execução
2026-06-10 10:30:05 | INFO | EXTRACT | Extração concluída
```

### 3. Finalização

```python
monitor.end_execution(records_processed=1000, status='success')
```

### 4. Persistência

Os dados são salvos automaticamente em:
- **CSV**: `monitoring/execution_history.csv`
- **PostgreSQL**: `audit.pipeline_execution`

## Estrutura de Logs

### Formato

```
YYYY-MM-DD HH:MM:SS | LEVEL | PROCESS | Message
```

### Exemplos

```
2026-06-10 10:30:00 | INFO | PIPELINE | Iniciando execução da pipeline
2026-06-10 10:30:05 | INFO | EXTRACT | Extração concluída com sucesso
2026-06-10 10:30:10 | ERROR | CURATED | Falha ao processar dados
2026-06-10 10:30:15 | WARNING | ANALYTICS | Dados inconsistentes detectados
```

### Níveis de Severidade

- **INFO**: Informações gerais de execução
- **WARNING**: Alertas não críticos
- **ERROR**: Erros que não interrompem a execução
- **CRITICAL**: Erros críticos que interrompem a execução

## Auditoria PostgreSQL

### Schema Audit

```sql
CREATE SCHEMA audit;
```

### Tabela pipeline_execution

```sql
CREATE TABLE audit.pipeline_execution (
    id_execucao VARCHAR(36) PRIMARY KEY,
    inicio_execucao TIMESTAMP NOT NULL,
    fim_execucao TIMESTAMP,
    duracao_segundos NUMERIC(10, 2),
    status VARCHAR(20) NOT NULL,
    registros_processados INTEGER DEFAULT 0,
    camada VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Índices

- `idx_pipeline_execution_inicio_execucao`: Consultas por data
- `idx_pipeline_execution_status`: Consultas por status
- `idx_pipeline_execution_camada`: Consultas por camada
- `idx_pipeline_execution_created_at`: Consultas recentes

## Exemplos de Auditoria

### Consultar Últimas Execuções

```sql
SELECT 
    id_execucao,
    camada,
    inicio_execucao,
    fim_execucao,
    duracao_segundos,
    status,
    registros_processados
FROM audit.pipeline_execution
ORDER BY inicio_execucao DESC
LIMIT 20;
```

### Consultar Execuções por Camada

```sql
SELECT 
    camada,
    COUNT(*) as total_execucoes,
    AVG(duracao_segundos) as tempo_medio,
    SUM(registros_processados) as total_registros
FROM audit.pipeline_execution
WHERE inicio_execucao >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY camada
ORDER BY total_execucoes DESC;
```

### Consultar Taxa de Sucesso

```sql
SELECT 
    camada,
    COUNT(*) as total,
    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as sucesso,
    ROUND(SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as taxa_sucesso
FROM audit.pipeline_execution
WHERE inicio_execucao >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY camada;
```

### Consultar Execuções Falhadas

```sql
SELECT 
    id_execucao,
    camada,
    inicio_execucao,
    duracao_segundos,
    registros_processados
FROM audit.pipeline_execution
WHERE status = 'failed'
    AND inicio_execucao >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY inicio_execucao DESC;
```

## Como Consultar Histórico

### Via CSV

```python
import pandas as pd
from monitoring.pipeline_monitor import PipelineMonitor

monitor = PipelineMonitor()
history = monitor.get_execution_history(limit=100)
print(history)
```

### Via PostgreSQL

```python
import pandas as pd
from monitoring.pipeline_monitor import PipelineMonitor

monitor = PipelineMonitor()
history = monitor.get_execution_history_from_db(limit=100)
print(history)
```

### Via SQL Direto

```bash
psql -h localhost -p 5434 -U admin -d portfolio_db -c "
SELECT * FROM audit.pipeline_execution 
ORDER BY inicio_execucao DESC 
LIMIT 20;
"
```

## Como Visualizar Métricas

### Métricas de Qualidade de Dados

```python
import pandas as pd

metrics_file = 'analytics/data_quality_metrics.parquet'
df = pd.read_parquet(metrics_file)
print(df)
```

### Métricas Disponíveis

- `total_clientes`: Total de clientes
- `total_produtos`: Total de produtos
- `total_pedidos`: Total de pedidos
- `total_itens`: Total de itens de pedido
- `percentual_integridade_geral`: Integridade geral (%)
- `percentual_nulos_*`: Percentual de nulos por entidade
- `percentual_duplicados_*`: Percentual de duplicados por entidade
- `data_execucao`: Timestamp da execução

## Integração com run_pipeline.py

A pipeline principal foi atualizada para incluir monitoramento automático:

```python
def run_extract(self) -> bool:
    monitor = PipelineMonitor()
    monitor.start_execution('extract')
    
    try:
        # Executa extract
        monitor.end_execution(status='success')
        return True
    except Exception as e:
        monitor.end_execution(status='failed')
        return False
```

Cada etapa da pipeline (extract, curated, load_dw, analytics, tests) agora registra:
- Início da execução
- Fim da execução
- Duração em segundos
- Status (success/failed)
- Registros processados

## Integração com Airflow

O DAG foi atualizado com uma nova task:

```python
monitor_task = BashOperator(
    task_id='monitor_task',
    bash_command='python3 analytics/generate_data_quality_metrics.py',
    dag=dag,
)
```

Fluxo atualizado:
```
extract >> curated >> analytics >> quality >> monitor >> tests
```

## Testes Automatizados

Novos testes adicionados ao `test_project.py`:

1. **test_logs_created**: Verifica se arquivos de log existem
2. **test_audit_schema_exists**: Verifica se schema audit existe
3. **test_pipeline_execution_table_exists**: Verifica se tabela pipeline_execution existe
4. **test_execution_history_csv_exists**: Verifica se execution_history.csv existe
5. **test_data_quality_metrics_exists**: Verifica se data_quality_metrics.parquet existe
6. **test_monitoring_functioning**: Verifica se sistema de monitoramento funciona

## Executar Testes

```bash
python3 test_project.py
```

## Inicializar Audit Schema

```bash
psql -h localhost -p 5434 -U admin -d portfolio_db -f sql/audit/create_audit_schema.sql
```

## Gerar Métricas de Qualidade

```bash
python3 analytics/generate_data_quality_metrics.py
```

## Executar Pipeline com Monitoramento

```bash
python3 run_pipeline.py
```

## Dashboard de Observabilidade

Consulte `docs/observability_dashboard.md` para:
- Consultas SQL para dashboard
- Indicadores chave (KPIs)
- Layout recomendado do dashboard
- Configuração do Metabase
- Thresholds de alerta

## Benefícios

1. **Visibilidade**: Rastreamento completo de todas as execuções
2. **Troubleshooting**: Logs estruturados facilitam debugging
3. **Auditoria**: Histórico completo em PostgreSQL
4. **Métricas**: Métricas de qualidade automaticamente calculadas
5. **Alertas**: Capacidade de configurar alertas baseados em métricas
6. **Performance**: Identificação de gargalos de performance
7. **Compliance**: Auditoria para requisitos de compliance

## Próximos Passos

1. **Alertas**: Configurar alertas automáticos para falhas
2. **Dashboard Metabase**: Criar dashboard visual no Metabase
3. **Anomaly Detection**: Implementar detecção de anomalias
4. **SLAs**: Definir e monitorar SLAs
5. **Cost Monitoring**: Monitorar custos de infraestrutura
6. **Real-time Metrics**: Implementar métricas em tempo real

## Critérios de Aceitação

✅ Logs são gerados automaticamente
✅ Histórico de execuções é armazenado (CSV + PostgreSQL)
✅ Auditoria está salva no PostgreSQL
✅ Airflow registra monitoramento
✅ Testes passam com sucesso
✅ Documentação está completa

## Resumo de Arquivos

### Arquivos Criados

1. `config/logging_config.py` - Configuração de logging estruturado
2. `monitoring/pipeline_monitor.py` - Módulo de monitoramento
3. `sql/audit/create_audit_schema.sql` - Script de criação do schema audit
4. `analytics/generate_data_quality_metrics.py` - Gerador de métricas
5. `docs/observability_dashboard.md` - Documentação do dashboard
6. `docs/sprint8_monitoring.md` - Este documento

### Arquivos Modificados

1. `airflow/dags/portfolio_pipeline.py` - Adicionada task monitor_task
2. `run_pipeline.py` - Adicionado monitoramento automático
3. `test_project.py` - Adicionados 6 novos testes

### Estrutura Final de Diretórios

```
portfolio-data-engineering/
├── config/
│   ├── settings.py
│   └── logging_config.py          # NOVO
├── logs/                          # NOVO
│   ├── pipeline.log
│   ├── quality.log
│   ├── analytics.log
│   └── airflow.log
├── monitoring/                    # NOVO
│   ├── pipeline_monitor.py
│   └── execution_history.csv
├── sql/
│   ├── ddl/
│   └── audit/                     # NOVO
│       └── create_audit_schema.sql
├── analytics/
│   ├── generate_data_quality_metrics.py  # NOVO
│   └── ...
├── airflow/
│   └── dags/
│       └── portfolio_pipeline.py  # MODIFICADO
├── docs/
│   ├── observability_dashboard.md  # NOVO
│   └── sprint8_monitoring.md      # NOVO
├── run_pipeline.py                # MODIFICADO
└── test_project.py                # MODIFICADO
```

## Comandos para Validação

### 1. Inicializar Audit Schema

```bash
psql -h localhost -p 5434 -U admin -d portfolio_db -f sql/audit/create_audit_schema.sql
```

### 2. Executar Pipeline Completa

```bash
python3 run_pipeline.py
```

### 3. Gerar Métricas de Qualidade

```bash
python3 analytics/generate_data_quality_metrics.py
```

### 4. Executar Testes

```bash
python3 test_project.py
```

### 5. Consultar Histórico de Execuções

```bash
psql -h localhost -p 5434 -U admin -d portfolio_db -c "
SELECT * FROM audit.pipeline_execution 
ORDER BY inicio_execucao DESC 
LIMIT 10;
"
```

### 6. Verificar Logs

```bash
tail -f logs/pipeline.log
tail -f logs/quality.log
tail -f logs/analytics.log
```

### 7. Verificar CSV de Execuções

```bash
cat monitoring/execution_history.csv
```

## Novos Testes Adicionados

1. **Teste 19**: Verificação de Arquivos de Log
   - Valida existência de pipeline.log, quality.log, analytics.log, airflow.log

2. **Teste 20**: Verificação do Schema Audit
   - Valida se schema audit existe no PostgreSQL

3. **Teste 21**: Verificação da Tabela pipeline_execution
   - Valida se tabela audit.pipeline_execution existe

4. **Teste 22**: Verificação do Arquivo execution_history.csv
   - Valida se arquivo CSV de histórico existe

5. **Teste 23**: Verificação do Arquivo data_quality_metrics.parquet
   - Valida se arquivo de métricas existe

6. **Teste 24**: Verificação do Sistema de Monitoramento
   - Valida import e instanciação do PipelineMonitor

Total de testes: 24 (18 originais + 6 novos)

## Conclusão

Sprint 8 foi concluído com sucesso, adicionando capacidades completas de observabilidade, monitoramento e logging ao projeto. A pipeline agora possui rastreamento completo de execuções, métricas de qualidade de dados, auditoria em PostgreSQL e integração com Airflow.

Todos os critérios de aceitação foram atendidos:
- ✅ Logs são gerados automaticamente
- ✅ Histórico de execuções é armazenado
- ✅ Auditoria está salva no PostgreSQL
- ✅ Airflow registra monitoramento
- ✅ Testes passam com sucesso
- ✅ Documentação está completa
