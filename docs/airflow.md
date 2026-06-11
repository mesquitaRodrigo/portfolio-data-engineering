# Apache Airflow Orchestration

## Overview

Apache Airflow has been integrated into the portfolio-data-engineering project to orchestrate the complete ETL pipeline. This document explains the architecture, DAG structure, scheduler configuration, and execution flow.

## Architecture

The Airflow integration follows a containerized approach using Docker Compose, ensuring consistency across development and production environments.

### Components

1. **PostgreSQL Database**: Shared database for both ERP data and Airflow metadata
2. **Airflow Webserver**: UI for monitoring DAGs and task execution
3. **Airflow Scheduler**: Responsible for scheduling and executing DAGs
4. **Airflow Init**: Initialization container for database setup and user creation

### Directory Structure

```
airflow/
├── dags/              # DAG definitions
│   └── portfolio_pipeline.py
├── logs/              # Task execution logs
├── plugins/           # Custom Airflow plugins
└── config/            # Airflow configuration files
```

## DAG: portfolio_pipeline

The `portfolio_pipeline` DAG orchestrates the complete data engineering pipeline with the following tasks:

### Task Dependencies

```
extract_task >> curated_task >> analytics_task >> quality_task >> tests_task
```

### Task Descriptions

1. **extract_task**
   - **Command**: `python3 etl/extract/extract_all_tables.py`
   - **Purpose**: Extract data from ERP PostgreSQL to Raw Layer (Parquet)
   - **Output**: Raw Layer files in `data/raw/`

2. **curated_task**
   - **Command**: `python3 etl/transform/build_curated_layer.py`
   - **Purpose**: Transform Raw Layer into dimensional model
   - **Output**: Curated Layer files in `data/curated/`
   - **Dependencies**: extract_task

3. **analytics_task**
   - **Command**: `python3 analytics/run_analytics.py`
   - **Purpose**: Calculate business metrics from Curated Layer
   - **Output**: Analytics Layer files in `data/analytics/`
   - **Dependencies**: curated_task

4. **quality_task**
   - **Command**: `python3 etl/quality/data_quality.py`
   - **Purpose**: Validate data quality across all layers
   - **Output**: Quality validation report
   - **Dependencies**: analytics_task

5. **tests_task**
   - **Command**: `python3 test_project.py`
   - **Purpose**: Run automated tests to verify pipeline integrity
   - **Output**: Test results and validation report
   - **Dependencies**: quality_task

### DAG Configuration

- **Schedule**: `@daily` (runs once per day)
- **Start Date**: 1 day ago
- **Retries**: 1 with 5-minute delay
- **Executor**: LocalExecutor
- **Catchup**: False (prevents backfilling)

## Scheduler

The Airflow Scheduler is responsible for:

1. **Parsing DAGs**: Reads DAG files from `airflow/dags/` directory
2. **Scheduling Tasks**: Determines when tasks should run based on schedule
3. **Task Queuing**: Queues tasks for execution by the executor
4. **Monitoring**: Tracks task status and handles retries

### Scheduler Configuration

- **Executor**: LocalExecutor (suitable for single-machine deployment)
- **Database**: PostgreSQL (shared with ERP)
- **DAGs Folder**: `/opt/airflow/dags`
- **Logs Folder**: `/opt/airflow/logs`

## Execution Flow

### Manual Execution

To manually trigger the DAG execution:

1. Access Airflow Webserver at `http://localhost:8080`
2. Navigate to the `portfolio_pipeline` DAG
3. Click "Trigger DAG" button
4. Monitor task execution in the "Grid View"

### Automated Execution

The DAG is scheduled to run daily at midnight. The scheduler will automatically:

1. Parse the DAG file
2. Create a DAG Run for the scheduled date
3. Execute tasks in dependency order
4. Handle failures and retries
5. Log execution details

### Task Execution

Each task uses `BashOperator` to execute Python scripts:

```python
extract_task = BashOperator(
    task_id='extract_task',
    bash_command='python3 etl/extract/extract_all_tables.py',
    dag=dag,
)
```

The working directory is set to the project root to ensure proper path resolution.

## Docker Compose

### Starting Airflow

```bash
docker-compose -f docker-compose-airflow.yml up -d
```

This command starts:
- PostgreSQL database (port 5434)
- Airflow Webserver (port 8080)
- Airflow Scheduler
- Airflow Init (runs once and exits)

### Stopping Airflow

```bash
docker-compose -f docker-compose-airflow.yml down
```

### Viewing Logs

```bash
# Webserver logs
docker logs airflow_webserver

# Scheduler logs
docker logs airflow_scheduler

# Task execution logs
ls -la airflow/logs/
```

### Accessing Web UI

1. Open browser to `http://localhost:8080`
2. Login with credentials:
   - Username: `admin`
   - Password: `admin`

## Monitoring

### DAG Status

- **Success**: All tasks completed successfully
- **Running**: Currently executing
- **Failed**: One or more tasks failed
- **Up for Retry**: Task will be retried

### Task Instance Details

Click on any task instance to view:
- Execution logs
- Duration
- Retry count
- XCom (cross-communication) data

### Logs Location

Task execution logs are stored in `airflow/logs/` with the following structure:

```
airflow/logs/
└── portfolio_pipeline/
    └── extract_task/
        └── <date>/
            └── <run_id>.log
```

## Troubleshooting

### Common Issues

1. **Task Fails with "Module not found"**
   - Ensure all dependencies are installed in the Airflow container
   - Check that the working directory is correctly set

2. **PostgreSQL Connection Error**
   - Verify PostgreSQL container is running
   - Check connection string in environment variables
   - Ensure database schema exists

3. **DAG Not Appearing in UI**
   - Check DAG file syntax
   - Verify DAG file is in `airflow/dags/` directory
   - Review scheduler logs for parsing errors

### Debug Mode

To enable debug logging, add to environment variables:

```yaml
AIRFLOW__LOGGING__LEVEL: DEBUG
```

## GitHub Actions Integration

The project includes CI/CD via GitHub Actions to automatically run tests on push and pull requests.

### Workflow Configuration

File: `.github/workflows/tests.yml`

**Triggers**:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Steps**:
1. Checkout code
2. Set up Python 3.10
3. Install dependencies
4. Wait for PostgreSQL service
5. Initialize database schema
6. Run `test_project.py`
7. Upload test results as artifacts

### Benefits

- **Automated Testing**: Ensures code quality before merging
- **Early Detection**: Catches issues early in development cycle
- **Consistency**: Runs tests in isolated environment
- **Artifact Storage**: Preserves test results for review

## Best Practices

1. **DAG Design**
   - Keep tasks idempotent (safe to re-run)
   - Use sensible retry policies
   - Set appropriate timeouts
   - Document task purposes

2. **Error Handling**
   - Implement proper error handling in Python scripts
   - Use meaningful error messages
   - Log important events
   - Handle edge cases

3. **Monitoring**
   - Regularly check DAG execution status
   - Review task logs for warnings
   - Monitor execution duration
   - Set up alerts for failures

4. **Security**
   - Change default passwords in production
   - Use environment variables for sensitive data
   - Restrict webserver access
   - Enable SSL/TLS for production

## Future Enhancements

Potential improvements for the Airflow integration:

1. **Dynamic Task Generation**: Create tasks dynamically based on configuration
2. **Sensor Tasks**: Add sensors to wait for external events
3. **Custom Operators**: Develop custom operators for specific tasks
4. **XCom Usage**: Pass data between tasks using XCom
5. **SubDAGs**: Break complex pipelines into SubDAGs
6. **Task Groups**: Organize related tasks into groups
7. **SLAs**: Add Service Level Agreements for monitoring
8. **Alerts**: Configure email/webhook notifications for failures
9. **Data Quality Sensors**: Integrate data quality checks as sensors
10. **Backfill Strategy**: Implement proper backfill for historical data

## References

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Airflow Docker Compose](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
