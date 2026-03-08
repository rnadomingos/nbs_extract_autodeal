import pandera as pa
from pandera.typing import Series, Index
from pandera import Field


class ServiceOrderServicesSchema(pa.DataFrameModel):
    """
    Schema for validating service order services data.

    Defines validation rules for services performed within a service order,
    including service codes, defect information, labor values, and related
    order references.
    """

    cod_empresa: Series[int] = Field(nullable=False)
    numero_os: Series[int] = Field(ge=0, nullable=False)
    codigo_servico: Series[str] = Field(nullable=True)
    cod_defeito: Series[str] = Field(nullable=True)
    descricao: Series[str] = Field(nullable=True)

    valor_mdo_os: Series[float] = Field(ge=0, nullable=True)
    valor_oc: Series[str] = Field(nullable=True)
    quantidade_oc: Series[str] = Field(nullable=True)
    nr_sg: Series[str] = Field(nullable=True)

    # Index validation
    __index__: Index[int] = Field(
        ge=0, 
        nullable=False
    )

    class Config:
        coerce = True
        strict = False