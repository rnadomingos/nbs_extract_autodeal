import pandera.pandas as pa
from pandera.typing import Series, Index
from pandera import Field


class ItemsServiceOrderSchema(pa.DataFrameModel):
    """
    Schema for validating service order items data.

    Ensures correct typing and value constraints for service order
    item-level information, including financial and defect details.
    """

    cod_empresa: Series[int] = Field(nullable=False)
    numero_os: Series[int] = Field(ge=0, nullable=False)
    cod_item: Series[str] = Field(nullable=True)
    cod_defeito: Series[str] = Field(nullable=True)
    descricao_defeito: Series[str] = Field(nullable=True)
    valor_os: Series[float] = Field(ge=0, nullable=True)
    valor_oc: Series[str] = Field(nullable=True)
    quantidade_oc: Series[str] = Field(nullable=True)
    nr_sg: Series[str] = Field(nullable=True)

    # DataFrame index validation
    __index__: Index[int] = Field(
        ge=0,
        nullable=False
    )

    class Config:
        coerce = True
        strict = False