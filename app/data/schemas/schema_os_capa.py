import pandera.pandas as pa
from pandera.typing import Series
from datetime import datetime


class OSCapaSchema(pa.DataFrameModel):
    """
    Schema para validação dos dados da OS Capa.

    Attributes: 
        cod_empresa (Series[int]): Identificador da Empresa
    """

    cod_empresa: Series[int] = pa.Field(
        ge=2, le=3
    )
    numero_os: Series[int] = pa.Field(ge=0)
    os_original: Series[str]
    data_emissao: Series[datetime] = pa.Field(ge="2024-10-21")
    data_encerramento: Series[str] = pa.Field(nullable=True)
    data_cancelamento: Series[str] = pa.Field(nullable=True)
    razao_social: Series[str]
    tipo_os: Series[str]
    responsavel: Series[str]
    chassi: Series[str]
    veic_modelo: Series[str]
    ano: Series[str]
    km: Series[int] = pa.Field(ge=0)
    placa: Series[str] = pa.Field(nullable=True)
    data_venda: Series[datetime] = pa.Field(ge="1899-12-30", nullable=True)
    status_os: Series[str]
    numero_do_dealer: Series[str]
    razao_social_dealer: Series[str]
    valor_estimado_os: Series[float] = pa.Field(ge=0)

    class Config:
        coerce = True
        strict = True
        unique_column_names = False