-- Validation Query: Count produtos
-- Verifica a quantidade de registros na tabela produtos

SELECT 
    'produtos' as tabela,
    COUNT(*) as total_registros,
    MIN(id_produto) as menor_id,
    MAX(id_produto) as maior_id,
    COUNT(DISTINCT categoria) as categorias_unicas
FROM produtos;
