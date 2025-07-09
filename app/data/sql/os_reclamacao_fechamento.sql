-- SCRIPT PARA ATUALIZAR AS RECLAMACOES DAS OSs ENCERRADAS NA TABELA OS_RECLAMACOES
SELECT  
      --ORDER DE SERVICO
      os.cod_empresa,
      os.numero_os,
      --RECLAMACAO_FEITA_PELO_CLIENTE
      TRIM(UPPER(OS_ORIGINAL.DESCRICAO)) as reclamacao,
      OS_ORIGINAL.Item
FROM  os 
      inner join os_tipos ostp on (os.tipo = ostp.tipo)
      left join OS_ORIGINAL on (OS_ORIGINAL.NUMERO_OS = os.numero_os and OS_ORIGINAL.COD_EMPRESA = os.cod_empresa)             
-- WHERE to_char(os.data_encerrada,'dd/MM/YYYY')= to_char(sysdate,'dd/MM/YYYY') -- PARA UTILIZAR NA ROTINA AUTOMATICA
where os.data_emissao >= '01/07/2025'
AND nvl(ostp.garantia,'N') = 'S'
AND os.cod_empresa IN (2,3,4)
and nvl(upper(os.orcamento),'N') = 'N'
AND OS.NUMERO_OS > 0
order by os.cod_empresa,os.numero_os,OS_ORIGINAL.ITEM asc