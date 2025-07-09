-- SCRIPT PARA ATUALIZAR O STATUS DAS OSs CANCELADAS
SELECT 
    -- ORDEM DE SERVIÇO
    os.cod_empresa,
    CASE 
        WHEN NVL(os.complemento, 'N') = 'N' THEN 'S'
        ELSE 'N'
    END AS os_original,
    os.numero_os,
    os.data_emissao AS data_emissao,
    os.data_encerrada AS data_encerramento,
    os.data_cancelamento AS data_cancelamento,
    TRIM(UPPER(emp.empresa_nome_completo)) AS razao_social,
    CONCAT(CONCAT(TRIM(UPPER(ostp.tipo)), ' - '), TRIM(UPPER(ostp.descricao))) AS tipo_os,
    TRIM(UPPER(usu2.nome_completo)) AS responsavel,

    -- VEÍCULO
    TRIM(UPPER(dados.chassi)) AS chassi,
    CONCAT(CONCAT(TRIM(UPPER(marcas.marca_abrac)), ' - '), TRIM(UPPER(modelo.descricao_modelo))) AS veic_modelo,
    TRIM(UPPER(dados.ano)) AS ano,
    dados.km AS km,
    TRIM(UPPER(dados.placa)) AS placa,
    (
        SELECT MAX(frota.data_compra)
        FROM clientes_frota frota
        WHERE frota.cod_produto = dados.cod_produto
          AND frota.cod_modelo = dados.cod_modelo
          AND frota.chassi = dados.chassi
          AND frota.cod_cliente = os.cod_cliente
    ) AS data_venda,
    CASE
        WHEN os.status_os = '0' THEN 'ABERTA'
        WHEN os.status_os = '1' THEN 'FECHADA'
        ELSE 'CANCELADA'
    END AS status_os,
    SYSDATE, -- updated_at

    -- DEALER
    CASE 
        WHEN marcas.cod_marca IN ('1', '336') AND os.cod_empresa = '2' THEN '41261'
        WHEN marcas.cod_marca IN ('65') AND os.cod_empresa = '2' THEN '41262'
        WHEN marcas.cod_marca IN ('1', '336') AND os.cod_empresa = '3' THEN '40998'
        WHEN marcas.cod_marca IN ('65') AND os.cod_empresa = '3' THEN '47877'
        WHEN marcas.cod_marca IN ('65') AND os.cod_empresa = '4' THEN '47940'
        ELSE '0'
    END AS numero_do_dealer,
    TRIM(UPPER(emp.empresa_nome_completo)) AS razao_social_dealer

FROM os
INNER JOIN produtos prod ON os.cod_produto = prod.cod_produto
INNER JOIN produtos_modelos modelo ON os.cod_produto = modelo.cod_produto AND os.cod_modelo = modelo.cod_modelo
INNER JOIN empresas emp ON os.cod_empresa = emp.cod_empresa
INNER JOIN clientes cli ON os.cod_cliente = cli.cod_cliente
INNER JOIN os_tipos ostp ON os.tipo = ostp.tipo
LEFT JOIN empresas_usuarios usu2 ON os.quem_abriu = usu2.nome
LEFT JOIN marcas ON marcas.cod_marca = prod.cod_marca
LEFT JOIN os_dados_veiculos dados ON os.cod_empresa = dados.cod_empresa AND os.numero_os = dados.numero_os
-- LEFT JOIN os_relacoes ON os_relacoes.numero_os = os.numero_os AND os_relacoes.cod_empresa = os.cod_empresa
--WHERE to_char(os.Data_Cancelamento,'dd/MM/YYYY')= to_char(sysdate,'dd/MM/YYYY') -- SCRIPT PARA RODAR AUTOMATICAMENTE CONSIDERANDO A DATA E HORA DA EXECUÇÃO
WHERE os.data_cancelamento >= '01/07/2025'
  AND NVL(ostp.garantia, 'N') = 'S'
  AND os.cod_empresa IN ('2', '3', '4')
  AND NVL(UPPER(os.orcamento), 'N') = 'N'
-- AND os.numero_os > '0'
ORDER BY os.data_emissao, os.cod_empresa, os.numero_os;
