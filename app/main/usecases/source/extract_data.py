from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import TextClause
from infra.oracle_database import engine
from typing import TypeVar, Dict

import pandera.pandas as pa
import pandas as pd

Base = declarative_base()

#TypeVar to data_model
BaseModel = TypeVar("T", bound=Base) # type: ignore

class ExtractData:
    def __init__(
              self,
              query:TextClause,
              query_params:Dict,
              schema: pa.DataFrameModel,
              lazy: bool = True
              ) -> None:
         self.query = query
         self.query_params = query_params
         self.schema = schema
         self.lazy = lazy
    
    def get_data_nbs(self) -> pd.DataFrame:
        """
        Executes a SQL query and returns the result as a validated DataFrame.

        This method runs a parameterized SQL query using SQLAlchemy, retrieves the result
        as a pandas DataFrame, and validates it against the provided Pandera schema model.

        Args:
            query (TextClause): A SQLAlchemy text clause representing the SQL query to execute.
            params (Dict): A dictionary of parameters to pass to the SQL query.
            schema (pa.DataFrameModel): A Pandera schema model used to validate the output DataFrame.
            lazy (bool, optional): If True, collects all validation errors before raising. Defaults to True.

        Returns:
            pd.DataFrame: The resulting DataFrame from the SQL query, validated against the given schema.

        Raises:
            SQLAlchemyError: If an error occurs during the SQL execution.
            SchemaError: If the DataFrame does not conform to the provided schema.
        """
        try:
            with engine.connect() as conn, conn.begin():
                dataframe = pd.read_sql(self.query, conn, params=self.query_params) 
                validate_df = self.schema.to_schema().validate(dataframe, lazy=self.lazy)
                return validate_df                
        except SQLAlchemyError as e:
                print("Erro ao carregar os dados:")
                print(e.__class__.__name__, "-", e._message)
                raise
        return pd.DataFrame()
