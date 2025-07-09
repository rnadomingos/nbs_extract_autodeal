-- SCRIPT PARA INSERIR AS NFs DAS OSs NA TABELA os_nota_fiscal
SELECT 
    -- ORDEM DE SERVIÇO
    os.cod_empresa,
    os.numero_os,
    
    -- NOTA FISCAL
    '' AS nr_sg,
    CASE 
        WHEN vendas.nfe = 'S' THEN '1'
        ELSE '2' 
    END AS tipo_nota_fiscal,
    vendas.controle AS nr_nota_fiscal,
    vendas.emissao AS data_referencia,
    vendas.total_nota AS valor
FROM os
INNER JOIN os_tipos ostp 
    ON os.tipo = ostp.tipo
LEFT JOIN vendas 
    ON vendas.cod_empresa = os.cod_empresa 
    AND vendas.numero_os = os.numero_os
LEFT JOIN operacoes 
    ON operacoes.cod_empresa = vendas.cod_empresa 
    AND operacoes.cod_operacao = vendas.cod_operacao
---WHERE to_char(os.data_emissao,'dd/MM/YYYY')= to_char(sysdate,'dd/MM/YYYY') -- PARA UTILIZAR NA ROTINA AUTOMATICA
WHERE os.data_emissao >= '01/07/2025'
  AND os.status_os = '0'
  AND NVL(ostp.garantia, 'N') = 'S'
  AND os.cod_empresa IN (2, 3, 4)
  AND NVL(UPPER(os.orcamento), 'N') = 'N'
  --AND OS.NUMERO_OS>'0'
ORDER BY 
    os.cod_empresa,
    os.numero_os;
