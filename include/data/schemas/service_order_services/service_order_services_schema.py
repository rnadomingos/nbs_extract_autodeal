import pandera.pandas as pa
from pandera.typing import Index
from pandera import Field


class ServiceOrderServicesSchema(pa.DataFrameModel):
    """
    Schema for validating service order services data.

    Defines validation rules for services performed within a service order,
    including service codes, defect information and labor values.
    """

    cod_empresa: int = Field(nullable=False)
    numero_os: int = Field(ge=0, nullable=False)
    item: int = Field(nullable=True)
    codigo_servico: str = Field(nullable=True)
    cod_defeito: str = Field(nullable=True)
    descritivo: str = Field(nullable=True)
    valor: float = Field(ge=0, nullable=True)

    # Index validation
    __index__: Index[int] = Field(ge=0, nullable=False)

    class Config:
        coerce = True
        strict = False
