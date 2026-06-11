-- Audit Schema Creation Script
-- Creates the audit schema and pipeline_execution table for tracking pipeline executions

-- Create audit schema
CREATE SCHEMA IF NOT EXISTS audit;

-- Create pipeline_execution table
CREATE TABLE IF NOT EXISTS audit.pipeline_execution (
    id_execucao VARCHAR(36) PRIMARY KEY,
    inicio_execucao TIMESTAMP NOT NULL,
    fim_execucao TIMESTAMP,
    duracao_segundos NUMERIC(10, 2),
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'running', 'success', 'failed', 'partial')),
    registros_processados INTEGER DEFAULT 0,
    camada VARCHAR(50) NOT NULL CHECK (camada IN ('extract', 'curated', 'analytics', 'quality', 'tests', 'monitor')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_pipeline_execution_inicio_execucao ON audit.pipeline_execution(inicio_execucao DESC);
CREATE INDEX IF NOT EXISTS idx_pipeline_execution_status ON audit.pipeline_execution(status);
CREATE INDEX IF NOT EXISTS idx_pipeline_execution_camada ON audit.pipeline_execution(camada);
CREATE INDEX IF NOT EXISTS idx_pipeline_execution_created_at ON audit.pipeline_execution(created_at DESC);

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION audit.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_pipeline_execution_updated_at
    BEFORE UPDATE ON audit.pipeline_execution
    FOR EACH ROW
    EXECUTE FUNCTION audit.update_updated_at_column();

-- Grant permissions (adjust as needed for your environment)
-- GRANT SELECT, INSERT, UPDATE ON audit.pipeline_execution TO admin;
-- GRANT USAGE, SELECT ON SEQUENCE audit.pipeline_execution_id_execucao_seq TO admin;

COMMENT ON SCHEMA audit IS 'Audit schema for pipeline execution tracking and monitoring';
COMMENT ON TABLE audit.pipeline_execution IS 'Stores execution history and metrics for pipeline runs';
COMMENT ON COLUMN audit.pipeline_execution.id_execucao IS 'Unique identifier for each pipeline execution (UUID)';
COMMENT ON COLUMN audit.pipeline_execution.inicio_execucao IS 'Timestamp when the pipeline execution started';
COMMENT ON COLUMN audit.pipeline_execution.fim_execucao IS 'Timestamp when the pipeline execution ended';
COMMENT ON COLUMN audit.pipeline_execution.duracao_segundos IS 'Total duration of the execution in seconds';
COMMENT ON COLUMN audit.pipeline_execution.status IS 'Execution status: pending, running, success, failed, partial';
COMMENT ON COLUMN audit.pipeline_execution.registros_processados IS 'Number of records processed during execution';
COMMENT ON COLUMN audit.pipeline_execution.camada IS 'Pipeline layer: extract, curated, analytics, quality, tests, monitor';
COMMENT ON COLUMN audit.pipeline_execution.created_at IS 'Record creation timestamp';
COMMENT ON COLUMN audit.pipeline_execution.updated_at Is 'Record last update timestamp';
