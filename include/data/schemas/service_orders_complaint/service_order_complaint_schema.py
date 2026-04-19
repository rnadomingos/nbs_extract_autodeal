import pandera.pandas as pa
from pandera.typing import Series, Index
from pandera import Field


class ServiceOrdersComplaintSchema(pa.DataFrameModel):
    """
    Schema for validating service order complaint data.

    This schema validates customer complaints registered for service orders,
    ensuring correct company code, service order number, complaint text,
    and associated item number.
    """

    cod_empresa: Series[int] = Field(nullable=False)
    numero_os: Series[int] = Field(ge=0, nullable=False)
    reclamacao: Series[str] = Field(nullable=False)
    item: Series[int] = Field(ge=1,nullable=False)
    # Index validation
    __index__: Index[int] = Field(
        ge=0,
        nullable=False
    )

    class Config:
        coerce = True
        strict = False