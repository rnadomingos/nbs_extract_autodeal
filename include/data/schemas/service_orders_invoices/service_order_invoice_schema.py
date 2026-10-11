import pandera.pandas as pa
from pandera.typing import Index
from pandera import Field
from pandas import Timestamp


class ServiceOrdersInvoice(pa.DataFrameModel):
    """
    Schema for validating service order invoice data.

    Ensures correct validation of invoice-related information associated
    with service orders, including fiscal details, reference dates, and values.
    """

    cod_empresa: int = Field(ge=0, nullable=False)

    numero_os: int = Field(ge=0, nullable=False)

    nr_sg: str = Field(nullable=True)

    tipo_nota_fiscal: str = Field(nullable=False)

    nr_nota_fiscal: int = Field(nullable=True)

    data_referencia: pa.DateTime = Field(nullable=True)

    valor: float = Field(ge=0, nullable=True)

    # Index validation
    __index__: Index[int] = Field(ge=0, le=1361, nullable=False)

    class Config:
        coerce = True
        strict = False
