from sqlalchemy import text

stmt_open_items_service_orders = text ("""
SELECT 
    -- ORDER DE SERVIÇO
    os.cod_empresa,
    os.numero_os,
    -- PEÇAS E LUBRIFICANTES
    os_requisicoes.cod_item AS cod_item,
    '' AS cod_defeito,
    -- os_requisicoes.item AS cod_defeito,
    itens.descricao AS descricao_defeito,
    -- os_requisicoes.preco_garantia AS valor_os,
    CASE
        WHEN os_tipos_empresas.tipo_preco_peca = 'G' 
            THEN (os_requisicoes.preco_garantia * os_requisicoes.quantidade)
        ELSE (os_requisicoes.preco_original * os_requisicoes.quantidade)
    END AS valor_os,
    -- (os_requisicoes.preco_original * os_requisicoes.quantidade) AS valor_os,
    '' AS valor_oc,
    '' AS quantidade_oc,
    -- os_requisicoes.quantidade AS quantidade_oc,
    '' AS nr_sg
FROM os
    INNER JOIN os_tipos ostp 
        ON os.tipo = ostp.tipo
    INNER JOIN os_requisicoes 
        ON os_requisicoes.cod_empresa = os.cod_empresa
        AND os_requisicoes.numero_os = os.numero_os
    INNER JOIN itens 
        ON os_requisicoes.cod_item = itens.cod_item
    INNER JOIN os_tipos_empresas 
        ON os_tipos_empresas.cod_empresa = os.cod_empresa
        AND os_tipos_empresas.tipo = os.tipo

WHERE TO_CHAR(os.data_emissao, 'YYYY-MM-DD') >= :max_date
  AND os.status_os = '0'
  AND NVL(ostp.garantia, 'N') = 'S'
  AND os.cod_empresa IN (2, 3, 4)
  AND NVL(UPPER(os.orcamento), 'N') = 'N'
  AND os.numero_os > 0
""")