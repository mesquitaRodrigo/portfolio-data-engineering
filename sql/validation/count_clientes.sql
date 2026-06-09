-- Validation Query: Count clientes
-- Verifica a quantidade de registros na tabela clientes

SELECT 
    'clientes' as tabela,
    COUNT(*) as total_registros,
    MIN(id_cliente) as menor_id,
    MAX(id_cliente) as maior_id
FROM clientes;
