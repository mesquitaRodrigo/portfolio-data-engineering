"""
Portfolio Data Pipeline DAG
Orchestrates the complete ETL pipeline: ERP → Raw → Curated → Analytics → Quality → Monitor → Tests

This DAG implements the complete data engineering pipeline for the portfolio project:
- Extract: Extract data from ERP PostgreSQL to Raw Layer (Parquet)
- Curated: Transform Raw Layer into dimensional model
- Analytics: Calculate business metrics from Curated Layer
- Quality: Validate data quality across all layers
- Monitor: Track pipeline execution metrics and generate quality metrics
- Tests: Run automated tests to verify pipeline integrity

Dependencies:
extract_task >> curated_task >> analytics_task >> quality_task >> monitor_task >> tests_task
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

# Default arguments for the DAG
default_args = {
    'owner': 'data-engineer',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # Set working directory to project root
    'cwd': '/opt/airflow/dags/../..',
}

# Create the DAG
dag = DAG(
    'portfolio_pipeline',
    default_args=default_args,
    description='Complete ETL Pipeline: ERP → Raw → Curated → Analytics → Quality → Tests',
    schedule_interval='@daily',  # Run daily
    catchup=False,
    tags=['etl', 'portfolio', 'data-engineering'],
)

# Task 1: Extract data from ERP to Raw Layer
extract_task = BashOperator(
    task_id='extract_task',
    bash_command='python3 etl/extract/extract_all_tables.py',
    dag=dag,
)

# Task 2: Build Curated Layer from Raw Layer
curated_task = BashOperator(
    task_id='curated_task',
    bash_command='python3 etl/transform/build_curated_layer.py',
    dag=dag,
)

# Task 3: Run Analytics on Curated Layer
analytics_task = BashOperator(
    task_id='analytics_task',
    bash_command='python3 analytics/run_analytics.py',
    dag=dag,
)

# Task 4: Run Data Quality checks
quality_task = BashOperator(
    task_id='quality_task',
    bash_command='python3 etl/quality/data_quality.py',
    dag=dag,
)

# Task 5: Generate data quality metrics and monitor pipeline
monitor_task = BashOperator(
    task_id='monitor_task',
    bash_command='python3 analytics/generate_data_quality_metrics.py',
    dag=dag,
)

# Task 6: Run automated tests
tests_task = BashOperator(
    task_id='tests_task',
    bash_command='python3 test_project.py',
    dag=dag,
)

# Define task dependencies
# extract_task must complete before curated_task
extract_task >> curated_task

# curated_task must complete before analytics_task
curated_task >> analytics_task

# analytics_task must complete before quality_task
analytics_task >> quality_task

# quality_task must complete before monitor_task
quality_task >> monitor_task

# monitor_task must complete before tests_task
monitor_task >> tests_task
