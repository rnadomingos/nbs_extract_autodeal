from sqlalchemy import text

stmt_closed_service_orders = text("""
WITH cte_frota_data_compra AS (
    SELECT 
        cod_produto,
        cod_modelo,
        chassi,
        cod_cliente,
        MAX(data_compra) AS data_venda
    FROM clientes_frota
    GROUP BY cod_produto, cod_modelo, chassi, cod_cliente
),
cte_ordem_servico AS (
    SELECT 
        -- ORDEM DE SERVIÇO
        os.cod_empresa,
        CASE 
            WHEN NVL(os.complemento, 'N') = 'N' THEN 'S'
            ELSE 'N' 
        END AS os_original,
        os.numero_os,
        TO_DATE(TO_CHAR(os.data_emissao, 'YYYY-MM-DD') || ' ' || os.hora_emissao, 'YYYY-MM-DD HH24:MI:SS') AS data_emissao,
        TO_DATE(TO_CHAR(os.data_encerrada, 'YYYY-MM-DD') || ' ' || os.hora_encerrada, 'YYYY-MM-DD HH24:MI:SS') AS data_encerramento,
        os.data_cancelamento,
        TRIM(UPPER(emp.empresa_nome_completo)) AS razao_social,
        CONCAT(CONCAT(TRIM(UPPER(ostp.tipo)), ' - '), TRIM(UPPER(ostp.descricao))) AS tipo_os,
        TRIM(UPPER(usu2.nome_completo)) AS responsavel,

        -- VEÍCULO
        TRIM(UPPER(dados.chassi)) AS chassi,
        CONCAT(CONCAT(TRIM(UPPER(marcas.marca_abrac)), ' - '), TRIM(UPPER(modelo.descricao_modelo))) AS veic_modelo,
        TRIM(UPPER(dados.ano)) AS ano,
        dados.km AS km,
        TRIM(UPPER(dados.placa)) AS placa,
        fdc.data_venda,
        CASE 
            WHEN os.status_os = '0' THEN 'ABERTA'
            WHEN os.status_os = '1' THEN 'FECHADA'
            ELSE 'CANCELADA'
        END AS status_os,
        -- DEALER
        CASE 
            WHEN marcas.cod_marca IN ('1', '336') AND os.cod_empresa = '2' THEN '41261'
            WHEN marcas.cod_marca IN ('65') AND os.cod_empresa = '2' THEN '41262'
            WHEN marcas.cod_marca IN ('1', '336') AND os.cod_empresa = '3' THEN '40998'
            WHEN marcas.cod_marca IN ('65') AND os.cod_empresa = '3' THEN '47877'
            WHEN marcas.cod_marca IN ('65') AND os.cod_empresa = '4' THEN '47940'
            ELSE '0'
        END AS numero_do_dealer,
        TRIM(UPPER(emp.empresa_nome_completo)) AS razao_social_dealer,
        NVL(
            (os.valor_servicos_bruto + os.valor_itens_bruto) - 
            (os.valor_desconto_serv - os.valor_desconto_item)
        ,0) AS valor_estimado_os

    FROM os
    INNER JOIN produtos prod ON os.cod_produto = prod.cod_produto
    INNER JOIN produtos_modelos modelo ON os.cod_produto = modelo.cod_produto AND os.cod_modelo = modelo.cod_modelo
    INNER JOIN empresas emp ON os.cod_empresa = emp.cod_empresa
    INNER JOIN clientes cli ON os.cod_cliente = cli.cod_cliente
    INNER JOIN os_tipos ostp ON os.tipo = ostp.tipo
    LEFT JOIN empresas_usuarios usu2 ON os.quem_abriu = usu2.nome
    LEFT JOIN marcas ON marcas.cod_marca = prod.cod_marca
    LEFT JOIN os_dados_veiculos dados ON os.cod_empresa = dados.cod_empresa AND os.numero_os = dados.numero_os
    LEFT JOIN cte_frota_data_compra fdc ON (fdc.cod_produto = dados.cod_produto
									        AND fdc.cod_modelo = dados.cod_modelo
									        AND fdc.chassi = dados.chassi
									        AND fdc.cod_cliente = os.cod_cliente)
	WHERE to_char(os.data_encerrada ,'YYYY-MM-dd') >= :max_date
        AND NVL(ostp.garantia, 'N') = 'S'
        AND os.cod_empresa IN ('2', '3', '4')
        AND NVL(UPPER(os.orcamento), 'N') = 'N'
)
SELECT *
FROM cte_ordem_servico
ORDER BY cod_empresa, numero_os""")
