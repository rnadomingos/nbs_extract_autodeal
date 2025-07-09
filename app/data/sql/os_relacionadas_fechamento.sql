-- SCRIPT PARA ATUALIZAR AS OSs RELACIONADAS DAS OSs ENCERRADAS NA TABELA OS_RELACIONADAS
SELECT 
    os.cod_empresa,
    os.numero_os,
    os_relacoes.numero_os_irma
FROM os
LEFT JOIN os_relacoes 
    ON os.cod_empresa = os_relacoes.cod_empresa 
    AND os.numero_os = os_relacoes.numero_os
INNER JOIN os_tipos ostp 
    ON os.tipo = ostp.tipo

--WHERE to_char(os.data_encerrada,'dd/MM/YYYY')= to_char(sysdate,'dd/MM/YYYY')  -- PARA UTILIZAR NA ROTINA AUTOMATICA
WHERE os.data_encerrada >= '01/07/2025'
  AND NVL(ostp.garantia, 'N') = 'S'
  AND os.cod_empresa IN ('2', '3', '4')
  --AND OS.NUMERO_OS>'0'
  AND NVL(UPPER(os.orcamento), 'N') = 'N'
ORDER BY 
    os.cod_empresa,
    os.numero_os;
