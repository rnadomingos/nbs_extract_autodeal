from sqlalchemy import text

stmt_open_service_order_services = text("""
    SELECT  
        -- ORDEM DE SERVIÇO
        os.cod_empresa,
        os.numero_os,   
        -- SERVIÇOS
        SUBSTR(os_servicos.cod_servico, 0, 11) AS codigo_servico,
        SUBSTR(os_servicos.item, 0, 10) AS cod_defeito,
        TRIM(UPPER(SUBSTR(serv.descricao_servico, 1, 160))) AS descricao_defeito,
        os_servicos.preco_venda AS valor_mdo_os,
        os_servicos.preco_liquido_final AS valor_oc,
        '' AS quantidade_oc,
        '' AS nr_sg
    FROM os
    INNER JOIN os_tipos ostp ON (os.tipo = ostp.tipo)
    INNER JOIN os_servicos ON (os_servicos.cod_empresa = os.cod_empresa AND os_servicos.numero_os = os.numero_os)
    INNER JOIN servicos serv ON (serv.cod_servico = os_servicos.cod_servico)
    WHERE to_char(os.data_emissao,'YYYY-MM-dd') >= :max_date
      AND os.status_os = '0'
      AND NVL(ostp.garantia, 'N') = 'S'
      AND os.cod_empresa IN (2, 3, 4)
      AND NVL(UPPER(os.orcamento), 'N') = 'N'
      AND OS.NUMERO_OS > 0
  """)