import pandera.pandas as pa
import pandas as pd
from pandera.typing import Series, Index
from pandera import Field


class RelatedServiceOrderSchema(pa.DataFrameModel):
    """
    Schema for validating related service order data.

    Validates company code, main service order number, and the related
    service order number with defined ranges and nullability rules.
    """

    cod_empresa: Series[int] = Field(ge=2, nullable=False)
    numero_os: Series[int] = Field(ge=0, nullable=False)
    numero_os_irma: Series[pd.Int64Dtype] = Field(ge=0, nullable=True, coerce=True)


    # Index validation
    __index__: Index[int] = Field(ge=0, nullable=False)

    class Config:
        coerce = True
        strict = False
