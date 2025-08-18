import pandera as pa
from pandera.typing import Series, Index
from pandera import Field


class RelatedServiceOrderSchema(pa.DataFrameModel):
    """
    Schema for validating related service order data.

    Validates company code, main service order number, and the related
    service order number with defined ranges and nullability rules.
    """

    cod_empresa: Series[int] = Field(ge=2, nullable=False)
    numero_os: Series[int] = Field(ge=72328, le=98864, nullable=False)
    numero_os_irma: Series[float] = Field(ge=66021, le=98868, nullable=True)

    # Index validation
    __index__: Index[int] = Field(ge=0, le=193, nullable=False)

    class Config:
        coerce = True
        strict = False
