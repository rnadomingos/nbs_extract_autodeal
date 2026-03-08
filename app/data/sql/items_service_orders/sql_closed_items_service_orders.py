from sqlalchemy import text

stmt_closed_items_service_orders = text ("""
SELECT
    -- ORDEM DE SERVIÇO
    os.cod_empresa,
    os.numero_os,
    os_requisicoes.cod_item              AS cod_item,
    ''                                   AS cod_defeito,
    itens.descricao                      AS descricao_defeito,
    (
        CASE
            WHEN os_tipos_empresas.tipo_preco_peca = 'G'
                THEN (os_requisicoes.preco_garantia * os_requisicoes.quantidade)
            ELSE
                (os_requisicoes.preco_final * os_requisicoes.quantidade)
        END
    )                                    AS valor_os,
    ''                                   AS valor_oc,
    ''                                   AS quantidade_oc,
    ''                                   AS nr_sg
FROM os
    INNER JOIN os_tipos ostp ON (ostp.tipo = os.tipo)
    INNER JOIN os_requisicoes ON (os_requisicoes.cod_empresa = os.cod_empresa AND os_requisicoes.numero_os  = os.numero_os)
    INNER JOIN itens ON (itens.cod_item = os_requisicoes.cod_item)
    INNER JOIN os_tipos_empresas ON (os_tipos_empresas.cod_empresa = os.cod_empresa AND os_tipos_empresas.tipo = os.tipo)
WHERE   TO_CHAR(os.data_encerrada, 'YYYY-MM-DD') >= :max_date
AND NVL(ostp.garantia, 'N') = 'S'
AND os.cod_empresa IN ('2', '3', '4')
AND NVL(UPPER(os.orcamento), 'N') = 'N'

ORDER BY
    os.cod_empresa,
    os.numero_os,
    os_requisicoes.cod_item
""")