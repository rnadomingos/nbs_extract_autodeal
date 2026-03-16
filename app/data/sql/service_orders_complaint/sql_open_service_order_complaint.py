from sqlalchemy import text

stmt_open_service_order_complaint = text("""
                          SELECT
                    os.cod_empresa,
                    os.numero_os,
                    TRIM(UPPER(os_original.descricao)) AS reclamacao,
                    os_original.item

                FROM os
                    INNER JOIN os_tipos ostp
                        ON os.tipo = ostp.tipo

                    LEFT JOIN os_original
                        ON os_original.numero_os = os.numero_os
                      AND os_original.cod_empresa = os.cod_empresa
                WHERE TO_CHAR(os.data_emissao, 'dd/MM/YYYY') > :max_date
                    AND os.status_os = '0'
                    AND NVL(ostp.garantia, 'N') = 'S'
                    AND os.cod_empresa IN (2, 3, 4)
                    -- AND os.numero_os > '0'
                    AND NVL(UPPER(os.orcamento), 'N') = 'N'

                ORDER BY
                    os.cod_empresa,
                    os.numero_os,
                    os_original.item
                                    """)
