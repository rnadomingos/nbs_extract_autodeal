from pandas import Timestamp
from pandera import DataFrameSchema, Column, Check, Index, MultiIndex

schema = DataFrameSchema(
    columns={
        "cod_empresa": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=2.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=3.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "numero_os": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=74651.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=104865.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "nr_sg": Column(
            dtype="object",
            checks=None,
            nullable=True,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "tipo_nota_fiscal": Column(
            dtype="object",
            checks=None,
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "nr_nota_fiscal": Column(
            dtype="int64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=51307.0, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=118732.0, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "data_referencia": Column(
            dtype="datetime64[ns]",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=Timestamp("2026-01-06 09:38:57"),
                    raise_warning=False,
                    ignore_na=True,
                ),
                Check.less_than_or_equal_to(
                    max_value=Timestamp("2026-03-16 18:39:59"),
                    raise_warning=False,
                    ignore_na=True,
                ),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "valor": Column(
            dtype="float64",
            checks=[
                Check.greater_than_or_equal_to(
                    min_value=6.62, raise_warning=False, ignore_na=True
                ),
                Check.less_than_or_equal_to(
                    max_value=56810.13, raise_warning=False, ignore_na=True
                ),
            ],
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
        "status": Column(
            dtype="object",
            checks=None,
            nullable=False,
            unique=False,
            coerce=False,
            required=True,
            regex=False,
            description=None,
            title=None,
        ),
    },
    checks=None,
    index=Index(
        dtype="int64",
        checks=[
            Check.greater_than_or_equal_to(
                min_value=0.0, raise_warning=False, ignore_na=True
            ),
            Check.less_than_or_equal_to(
                max_value=1361.0, raise_warning=False, ignore_na=True
            ),
        ],
        nullable=False,
        coerce=False,
        name=None,
        description=None,
        title=None,
    ),
    dtype=None,
    coerce=True,
    strict=False,
    name=None,
    ordered=False,
    unique=None,
    report_duplicates="all",
    unique_column_names=False,
    add_missing_columns=False,
    title=None,
    description=None,
)
