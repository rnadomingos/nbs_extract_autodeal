-- SCRIPT PARA ATUALIZAR OS SERVICOS DAS OSs NO FECHAMENTO NA TABELA OS_SERVICOS
SELECT  
    -- ORDEM DE SERVIÇO
    os.cod_empresa,
    os.numero_os,
    
    -- SERVIÇOS
    SUBSTR(os_servicos.cod_servico, 0, 11) AS codigo_servico,
    SUBSTR(os_servicos.item, 0, 10) AS cod_defeito,
    -- os_requisicoes.requisicao as cod_defeito,
    TRIM(UPPER(SUBSTR(serv.descricao_servico, 0, 160))) AS descricao,
    os_servicos.preco_venda AS valor_mdo_os,
    '' AS valor_oc,
    -- os_servicos.preco_liquido_final as valor_oc,
    -- serv.tempo_garantia as quantidade_oc,
    '' AS quantidade_oc,
    '' AS nr_sg

FROM os
INNER JOIN os_tipos ostp 
    ON os.tipo = ostp.tipo
LEFT JOIN os_servicos 
    ON os_servicos.cod_empresa = os.cod_empresa 
    AND os_servicos.numero_os = os.numero_os
LEFT JOIN servicos serv 
    ON serv.cod_servico = os_servicos.cod_servico

--WHERE to_char(os.data_encerrada,'dd/MM/YYYY')= to_char(sysdate,'dd/MM/YYYY') -- PARA UTILIZAR NA ROTINA AUTOMATICA
WHERE os.data_encerrada >= '01/07/2025'
  AND NVL(ostp.garantia, 'N') = 'S'
  AND os.cod_empresa IN (2, 3, 4)
  AND NVL(UPPER(os.orcamento), 'N') = 'N'

ORDER BY 
    os.cod_empresa,
    os.numero_os,
    os_servicos.item;
