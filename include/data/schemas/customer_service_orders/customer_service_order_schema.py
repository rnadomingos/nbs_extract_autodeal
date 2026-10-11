import pandera.pandas as pa
from pandera.typing import Index
from pandera import Field


class CustomerServiceOrderSchema(pa.DataFrameModel):
    """
    Schema for validating customer service order data.

    Validates key fields such as company code, order number, customer name,
    and contact information. Includes value constraints and nullability rules.
    """

    cod_empresa: int = Field(ge=2, nullable=False)
    numero_os: int = Field(ge=0, nullable=False)
    nome_cliente: str = Field(nullable=False)
    cpf_cnpj: str = Field(nullable=False)
    telefone: str = Field(nullable=True)
    celular: str = Field(nullable=True)

    # Índice do DataFrame
    __index__: Index[int] = Field(ge=0, nullable=False)

    class Config:
        coerce = True
        strict = False
        unique_column_names = False
