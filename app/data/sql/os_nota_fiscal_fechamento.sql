-- SCRIPT PARA ATUALIZAR AS NFs DAS OSs NO ENCERRAMENTO NA TABELA os_nota_fiscal
SELECT 
      --ORDER DE SERVICO
      os.cod_empresa,
      os.numero_os,
      
      --NOTA FISCAL
      '' as nr_sg,
      (CASE WHEN vendas.nfe='S' THEN '2'
      ELSE '1' END) AS tipo_nota_fiscal,
      vendas.controle AS nr_nota_fiscal,
      vendas.emissao AS data_referencia,
      vendas.total_nota AS valor,
      vendas.status
FROM  os 
      INNER JOIN os_tipos ostp ON (os.tipo = ostp.tipo)
      INNER JOIN vendas ON (vendas.cod_empresa = os.cod_empresa AND vendas.numero_os = os.numero_os)
      INNER JOIN operacoes ON (operacoes.cod_empresa = vendas.cod_empresa AND operacoes.cod_operacao = vendas.cod_operacao)
--WHERE to_char(os.data_encerrada,'dd/MM/YYYY') = to_char(sysdate,'dd/MM/YYYY') -- PARA UTILIZAR NA ROTINA AUTOMATICA     
where os.data_encerrada>='01/07/2025'
AND nvl(upper(ostp.garantia),'N')='S'
AND vendas.status!='1'
AND os.cod_empresa IN (2,3,4)
AND operacoes.Cod_Operacao='3'
ORDER BY os.cod_empresa,os.numero_os