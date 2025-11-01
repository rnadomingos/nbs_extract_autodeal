from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import TextClause
from infra.oracle_database import engine
from typing import TypeVar, Dict
from tqdm import tqdm
import pandera.pandas as pa
import pandas as pd


Base = declarative_base()

#TypeVar to data_model
BaseModel = TypeVar("T", bound=Base) # type: ignore

class ExtractData:
    def __init__(
              self,
              query:TextClause,
              query_params:Dict
              ) -> None:
         self.query = query
         self.query_params = query_params
    
    def get_data_nbs(self, schema: pa.DataFrameModel, lazy: bool = True) -> pd.DataFrame:
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
                tqdm.pandas()
                dataframe = pd.read_sql(self.query, conn, params=self.query_params) 
                validate_df = schema.to_schema().validate(dataframe, lazy=lazy)
                return validate_df                
        except SQLAlchemyError as e:
                print("Erro ao carregar os dados:")
                print(e.__class__.__name__, "-", e._message)
                raise
        return pd.DataFrame()
    
    def get_data_infer_schema_nbs(self) -> pd.DataFrame:
        """
        Executa a query SQL definida na instância e retorna o resultado como um DataFrame.

        Esta função estabelece uma conexão com o banco de dados usando o `engine`,
        executa a consulta SQL armazenada em `self.query` com os parâmetros `self.query_params`,
        e retorna o resultado em um objeto `pandas.DataFrame`.

        Caso ocorra um erro durante a execução da consulta, o erro é exibido no console
        e a exceção original é relançada.

        Returns:
            pd.DataFrame: DataFrame contendo os resultados da consulta.
            Retorna um DataFrame vazio se nenhum dado for obtido.

        Raises:
            SQLAlchemyError: Se ocorrer qualquer erro durante a execução da consulta SQL
            ou durante a conexão com o banco de dados.

        Example:
            >>> df = obj.get_data_infer_schema_nbs()
            >>> print(df.head())
        """
        try:
            with engine.connect() as conn, conn.begin():
                dataframe = pd.read_sql(self.query, conn, params=self.query_params) 
                return dataframe                
        except SQLAlchemyError as e:
                print("Erro ao carregar os dados:")
                print(e.__class__.__name__, "-", e._message)
                raise
        return pd.DataFrame()
