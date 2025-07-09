-- SCRIPT PARA INSERIR OS ITENS DAS OSs NA TABELA OS_ITENS
SELECT 
      --ORDER DE SERVICO
      os.cod_empresa,
      os.numero_os,
      
      --PECAS E LUBRIFICANTES
      os_requisicoes.cod_item as cod_item,
    '' as cod_defeito,
      --os_requisicoes.item as cod_defeito,
      itens.descricao as descr_defeito,
      --os_requisicoes.preco_garantia as valor_os,
      (case
       when os_tipos_empresas.tipo_preco_peca='G' then (os_requisicoes.preco_garantia * os_requisicoes.quantidade)
       ELSE (os_requisicoes.preco_original * os_requisicoes.quantidade) end) as valor_os,

      --(os_requisicoes.preco_original * os_requisicoes.quantidade) as valor_os,
    '' as valor_oc,
    '' as quantidade_oc,
      --os_requisicoes.quantidade as quantidade_oc,
    '' as nr_sg
      
   
FROM    os 
        inner join os_tipos ostp on (os.tipo = ostp.tipo)
        left join os_requisicoes on (os_requisicoes.cod_empresa = os.cod_empresa and os_requisicoes.numero_os = os.numero_os)
        left join itens on (os_requisicoes.cod_item = itens.cod_item)
        left join os_tipos_empresas on (os_tipos_empresas.cod_empresa = os.cod_empresa and os_tipos_empresas.tipo = os.tipo)


--WHERE to_char(os.data_emissao,'dd/MM/YYYY')= to_char(sysdate,'dd/MM/YYYY') -- PARA RODAR NO SCRIPT AUTOMATICO
where to_char(os.data_emissao,'dd/MM/YYYY') >= '01/07/2025'
and os.status_os='0'
AND nvl(ostp.garantia,'N')='S'
AND os.cod_empresa IN (2,3,4)
and nvl(upper(os.orcamento),'N')='N'
--AND OS.NUMERO_OS > 0