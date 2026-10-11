import pandera.pandas as pa
from pandera.typing import Series, Index
from pandera import Field


class ItemsServiceOrderSchema(pa.DataFrameModel):
    """
    Schema for validating service order items data.

    Ensures correct typing and value constraints for service order
    item-level information.
    """

    cod_empresa: int = Field(nullable=False)
    numero_os: int = Field(ge=0, nullable=False)
    item: int = Field(nullable=True)
    cod_servico: str = Field(nullable=True)
    cod_item: str = Field(nullable=True)
    descricao: str = Field(nullable=True)
    qtde_peca: int = Field(nullable=True)
    valor_os: float = Field(ge=0, nullable=True)

    # DataFrame index validation
    __index__: Index[int] = Field(ge=0, nullable=False)

    class Config:
        coerce = True
        strict = False
