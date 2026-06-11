# Observability Dashboard

## Overview

The Observability Dashboard provides comprehensive visibility into the data pipeline's health, performance, and data quality. This document outlines the key indicators, SQL queries, and metrics available for monitoring the portfolio-data-engineering platform.

## Key Indicators

### 1. Execuções por Dia (Daily Executions)

**Description**: Number of pipeline executions per day

**SQL Query**:
```sql
SELECT 
    DATE(inicio_execucao) as data,
    camada,
    COUNT(*) as total_execucoes,
    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as execucoes_sucesso,
    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as execucoes_falha
FROM audit.pipeline_execution
GROUP BY DATE(inicio_execucao), camada
ORDER BY data DESC, camada;
```

**Visualization**: Bar chart showing daily execution counts by layer

### 2. Tempo Médio da Pipeline (Average Pipeline Duration)

**Description**: Average execution time in seconds per layer

**SQL Query**:
```sql
SELECT 
    camada,
    AVG(duracao_segundos) as tempo_medio_segundos,
    MIN(duracao_segundos) as tempo_minimo_segundos,
    MAX(duracao_segundos) as tempo_maximo_segundos,
    STDDEV(duracao_segundos) as desvio_padrao_segundos
FROM audit.pipeline_execution
WHERE status = 'success'
    AND duracao_segundos IS NOT NULL
GROUP BY camada
ORDER BY tempo_medio_segundos DESC;
```

**Visualization**: Box plot or line chart showing duration distribution

### 3. Falhas por Período (Failures by Period)

**Description**: Number of failed executions by time period

**SQL Query**:
```sql
-- Last 7 days
SELECT 
    DATE(inicio_execucao) as data,
    camada,
    COUNT(*) as total_falhas,
    COUNT(DISTINCT id_execucao) as execucoes_unicas_falhadas
FROM audit.pipeline_execution
WHERE status = 'failed'
    AND inicio_execucao >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY DATE(inicio_execucao), camada
ORDER BY data DESC, camada;

-- Last 30 days by layer
SELECT 
    camada,
    COUNT(*) as total_falhas_30_dias,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentual_falhas
FROM audit.pipeline_execution
WHERE status = 'failed'
    AND inicio_execucao >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY camada
ORDER BY total_falhas_30_dias DESC;
```

**Visualization**: Heat map or trend line showing failure patterns

### 4. Volume Processado (Processed Volume)

**Description**: Total records processed by layer over time

**SQL Query**:
```sql
SELECT 
    DATE(inicio_execucao) as data,
    camada,
    SUM(registros_processados) as total_registros,
    AVG(registros_processados) as media_registros,
    MAX(registros_processados) as max_registros
FROM audit.pipeline_execution
WHERE status = 'success'
    AND registros_processados > 0
GROUP BY DATE(inicio_execucao), camada
ORDER BY data DESC, camada;

-- Cumulative volume
SELECT 
    camada,
    SUM(registros_processados) as volume_total,
    COUNT(*) as total_execucoes
FROM audit.pipeline_execution
WHERE status = 'success'
GROUP BY camada
ORDER BY volume_total DESC;
```

**Visualization**: Stacked bar chart or area chart showing volume trends

### 5. Qualidade dos Dados (Data Quality)

**Description**: Data quality metrics across all layers

**SQL Query**:
```sql
-- From data_quality_metrics.parquet (using DuckDB or direct query)
-- If loaded to PostgreSQL:
SELECT 
    data_execucao,
    total_clientes,
    total_produtos,
    total_pedidos,
    total_itens,
    percentual_integridade_geral,
    percentual_nulos_clientes,
    percentual_nulos_produtos,
    percentual_duplicados_clientes,
    percentual_duplicados_produtos
FROM analytics.data_quality_metrics
ORDER BY data_execucao DESC
LIMIT 30;

-- Quality trend
SELECT 
    DATE(data_execucao) as data,
    AVG(percentual_integridade_geral) as integridade_media,
    AVG(percentual_nulos_clientes) as nulos_media_clientes,
    AVG(percentual_duplicados_produtos) as duplicados_media_produtos
FROM analytics.data_quality_metrics
GROUP BY DATE(data_execucao)
ORDER BY data DESC;
```

**Visualization**: Gauge charts for current quality, trend lines for historical

## Advanced Queries

### Execution Success Rate

```sql
SELECT 
    camada,
    COUNT(*) as total_execucoes,
    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as sucesso,
    ROUND(SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as taxa_sucesso_percentual
FROM audit.pipeline_execution
WHERE inicio_execucao >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY camada
ORDER BY taxa_sucesso_percentual DESC;
```

### Slowest Executions

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
WHERE status = 'success'
    AND duracao_segundos IS NOT NULL
ORDER BY duracao_segundos DESC
LIMIT 10;
```

### Recent Execution History

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

### Layer Performance Comparison

```sql
SELECT 
    camada,
    COUNT(*) as total_execucoes,
    AVG(duracao_segundos) as tempo_medio,
    SUM(registros_processados) as total_registros,
    SUM(registros_processados) / NULLIF(AVG(duracao_segundos), 0) as registros_por_segundo
FROM audit.pipeline_execution
WHERE status = 'success'
    AND duracao_segundos > 0
GROUP BY camada
ORDER BY registros_por_segundo DESC;
```

### Error Patterns

```sql
SELECT 
    camada,
    status,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY camada), 2) as percentage
FROM audit.pipeline_execution
WHERE inicio_execucao >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY camada, status
ORDER BY camada, count DESC;
```

## Dashboard Layout Recommendations

### Top Row (Key Metrics)
1. **Total Executions Today**: Card showing count
2. **Success Rate**: Gauge chart (target: >95%)
3. **Average Duration**: Number card (seconds)
4. **Records Processed**: Number card (total)

### Middle Row (Trends)
1. **Daily Execution Trend**: Line chart (last 30 days)
2. **Layer Duration Comparison**: Bar chart
3. **Failure Rate Trend**: Line chart
4. **Data Quality Trend**: Line chart

### Bottom Row (Details)
1. **Recent Executions Table**: Last 20 executions
2. **Layer Performance**: Stacked bar chart
3. **Quality Metrics**: Gauge charts per entity
4. **Volume Processed**: Area chart

## Metabase Dashboard Setup

### Data Sources

1. **PostgreSQL - Audit Schema**
   - Table: `audit.pipeline_execution`
   - Connection: Use existing PostgreSQL connection

2. **Parquet - Data Quality Metrics**
   - File: `analytics/data_quality_metrics.parquet`
   - Connection: Use DuckDB or direct Parquet import

### Recommended Visualizations

1. **Execution Success Rate**
   - Type: Gauge
   - Query: Success rate by layer
   - Target: 95%+

2. **Pipeline Duration**
   - Type: Line chart
   - Query: Average duration over time
   - Time range: Last 30 days

3. **Data Quality Score**
   - Type: Gauge
   - Query: Overall integrity percentage
   - Target: 90%+

4. **Execution Volume**
   - Type: Bar chart
   - Query: Records processed by layer
   - Group by: Layer

5. **Failure Analysis**
   - Type: Table
   - Query: Failed executions with details
   - Columns: ID, layer, start time, duration

## Alert Thresholds

### Recommended Alerts

1. **High Failure Rate**
   - Condition: Success rate < 90% in last 24 hours
   - Severity: Critical
   - Action: Investigate immediately

2. **Long Execution Time**
   - Condition: Duration > 2x average for any layer
   - Severity: Warning
   - Action: Review performance

3. **Data Quality Drop**
   - Condition: Integrity < 85%
   - Severity: Warning
   - Action: Review data quality checks

4. **Zero Records Processed**
   - Condition: Records processed = 0 for any layer
   - Severity: Critical
   - Action: Investigate data source

## Performance Optimization

### Index Usage

The following indexes are available for optimal query performance:
- `idx_pipeline_execution_inicio_execucao` - For time-based queries
- `idx_pipeline_execution_status` - For status filtering
- `idx_pipeline_execution_camada` - For layer-based queries
- `idx_pipeline_execution_created_at` - For recent data queries

### Query Optimization Tips

1. Always filter by date range for large datasets
2. Use indexed columns in WHERE clauses
3. Avoid SELECT * on large tables
4. Use materialized views for complex aggregations
5. Consider partitioning by date for very large datasets

## Maintenance

### Data Retention

Recommended retention policies:
- Audit data: 90 days
- Execution history CSV: 90 days
- Data quality metrics: 180 days

### Cleanup Script

```sql
-- Delete audit records older than 90 days
DELETE FROM audit.pipeline_execution
WHERE inicio_execucao < CURRENT_DATE - INTERVAL '90 days';

-- Vacuum to reclaim space
VACUUM FULL audit.pipeline_execution;
```

## Future Enhancements

1. **Real-time Metrics**: Stream processing for live monitoring
2. **Anomaly Detection**: ML-based anomaly detection
3. **Predictive Analytics**: Forecast execution times
4. **Custom Alerts**: Webhook-based alerting
5. **Cross-pipeline Comparison**: Compare multiple pipeline runs
6. **Cost Monitoring**: Track infrastructure costs per execution
