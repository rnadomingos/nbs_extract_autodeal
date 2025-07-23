import pandera.pandas as pa
from pandera.typing import Series
from datetime import datetime


class OSCapaSchema(pa.DataFrameModel):
    """
    Validation schema for OS Capa data using Pandera.

    This schema defines the expected structure and constraints for the OS (Order of Service) header data.
    It is intended to validate pandas DataFrames loaded from external sources (e.g., SQL queries) to
    ensure data quality and type consistency before further processing.

    Attributes:
        cod_empresa (Series[int]): Company identifier. Must be either 2 or 3.
        numero_os (Series[int]): Service order number. Must be a non-negative integer.
        os_original (Series[str]): Indicates if the order is original.
        data_emissao (Series[datetime]): Emission date. Must be on or after 2024-10-21.
        data_encerramento (Series[str]): Closing date. Nullable.
        data_cancelamento (Series[str]): Cancellation date. Nullable.
        razao_social (Series[str]): Customer or company name.
        tipo_os (Series[str]): Type of service order.
        responsavel (Series[str]): Responsible person or technician.
        chassi (Series[str]): Vehicle chassis number.
        veic_modelo (Series[str]): Vehicle model.
        ano (Series[str]): Vehicle year.
        km (Series[int]): Vehicle mileage. Must be non-negative.
        placa (Series[str]): License plate. Nullable.
        data_venda (Series[datetime]): Sale date. Must be on or after 1899-12-30. Nullable.
        status_os (Series[str]): Status of the service order.
        numero_do_dealer (Series[str]): Dealer identification number.
        razao_social_dealer (Series[str]): Dealer name.
        valor_estimado_os (Series[float]): Estimated service order cost. Must be non-negative.

    Config:
        coerce (bool): Automatically convert column types where possible.
        strict (bool): Require that all defined columns exist in the input DataFrame.
        unique_column_names (bool): Disable check for unique column names.
    """
    cod_empresa: Series[int] = pa.Field(
        ge=2, le=3
    )
    numero_os: Series[int] = pa.Field(ge=0)
    os_original: Series[str]
    data_emissao: Series[datetime] = pa.Field(ge="2024-10-21")
    data_encerramento: Series[str] = pa.Field(nullable=True)
    data_cancelamento: Series[str] = pa.Field(nullable=True)
    razao_social: Series[str]
    tipo_os: Series[str]
    responsavel: Series[str]
    chassi: Series[str]
    veic_modelo: Series[str]
    ano: Series[str]
    km: Series[int] = pa.Field(ge=0)
    placa: Series[str] = pa.Field(nullable=True)
    data_venda: Series[datetime] = pa.Field(ge="1899-12-30", nullable=True)
    status_os: Series[str]
    numero_do_dealer: Series[str]
    razao_social_dealer: Series[str]
    valor_estimado_os: Series[float] = pa.Field(ge=0)

    class Config:
        coerce = True
        strict = True
        unique_column_names = False