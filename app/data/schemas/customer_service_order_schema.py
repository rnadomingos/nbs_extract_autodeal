import pandera.pandas as pa
from pandera.typing import Series, Index
from pandera import Field


class CustomerServiceOrderSchema(pa.DataFrameModel):
    """
    Schema for validating customer service order data.
    
    Validates key fields such as company code, order number, customer name,
    and contact information. Includes value constraints and nullability rules.
    """

    cod_empresa: Series[int] = Field(ge=2, nullable=False)
    numero_os: Series[int] = Field(ge=0, nullable=False)
    nome_cliente: Series[str] = Field(nullable=False)
    cpf_cnpj: Series[str] = Field(nullable=False)
    telefone: Series[str] = Field(nullable=True)
    celular: Series[str] = Field(nullable=True)

    # Índice do DataFrame
    __index__: Index[int] = Field(ge=0, nullable=False)

    class Config:
        coerce = True
        strict = False
        unique_column_names = False
