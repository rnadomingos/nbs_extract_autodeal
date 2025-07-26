-- SCRIPT PARA INSERIR OS CLIENTES DAS OSs 
SELECT 
      --ORDEM DE SERVICO
      os.cod_empresa,
      os.numero_os,
      --DADOS CLIENTE
      TRIM(UPPER(cli.nome)) AS NOME_CLIENTE,
      (case when length(cli.cod_cliente)='13' then concat('0',cli.cod_cliente)
       else to_char(cli.cod_cliente) end) CPF_CNPJ,
      --cli.cod_cliente AS CPF_CNPJ,
      '' as telefone,
      '' as celular   
FROM    os 
        inner join produtos prod on (os.cod_produto = prod.cod_produto)
        inner join produtos_modelos modelo on (os.cod_produto = modelo.cod_produto and os.cod_modelo = modelo.cod_modelo)
        inner join empresas emp on (os.cod_empresa = emp.cod_empresa)
        inner join clientes cli on (os.cod_cliente = cli.cod_cliente)
        inner join os_tipos ostp on (os.tipo = ostp.tipo)
        left join empresas_usuarios usu2 on (os.quem_abriu = usu2.nome)
        left join marcas on (marcas.cod_marca = prod.cod_marca)
        left join os_dados_veiculos dados on (os.cod_empresa = dados.cod_empresa and os.numero_os = dados.numero_os)
--WHERE to_char(os.data_emissao,'dd/MM/YYYY')= to_char(sysdate,'dd/MM/YYYY') -- PARA UTILIZAR NA ROTINA AUTOMÁTICA
where to_char(os.data_emissao,'dd/MM/YYYY')>='01/07/2025'
and os.status_os='0'
AND nvl(ostp.garantia,'N')='S'
AND os.cod_empresa IN (2,3,4)
and nvl(upper(os.orcamento),'N')='N'
AND OS.NUMERO_OS > 0