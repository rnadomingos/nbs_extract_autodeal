from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import TextClause, func
from infra.oracle_database import engine
from infra.postgres_database import SessionLocal
from typing import Type, TypeVar, Any, cast, Dict

import pandera.pandas as pa
import pandas as pd

Base = declarative_base()

#TypeVar to data_model
BaseModel = TypeVar("T", bound=Base) # type: ignore

class ExtractTransformLoad:
    """
    Class to execute and extract SQL queries from the NBS Oracle database
    and return a DataFrame with the Pandas library and load it into Postgres.
    """
    def view_max_date(self, date_column) -> dict: 
        """
        Get the maximum date from the given model's date column and format as 'yyyy-MM-dd'.
    
        Args:
            date_column: Column object from the model (e.g., data_model.data_cadastro).
        
        Returns:
            dict | None: Formatted max date as 'yyyy-MM-dd', or None if not found.
        """
        with SessionLocal() as db:
            try:
                result = db.query(func.max(date_column)).one()
                max_date = result[0]
                db.commit()
                if max_date:
                     return { 'max_date': max_date.strftime('%Y-%m-%d')}
                return { 'max_date': None }
            except SQLAlchemyError as e:
                db.rollback()
                print("Error load max date:")
                print(e.__class__.__name__, "-", str(e._message))
                raise
        return 

    def extract_sql_nbs(self, query: TextClause, params: Dict, schema: pa.DataFrameModel, lazy:bool = True) -> pd.DataFrame:
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
                dataframe = pd.read_sql(query, conn, params=params) 
                validate_df = schema.to_schema().validate(dataframe, lazy=lazy)
                return validate_df                
        except SQLAlchemyError as e:
                print("Erro ao carregar os dados:")
                print(e.__class__.__name__, "-", e._message)
                raise
        return pd.DataFrame()


    def transformDataFrame(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Converts datetime columns in the DataFrame to Python objects, replacing NaT values with None.

        This function is useful before inserting the data into a database using SQLAlchemy,
        since Pandas' NaT values can cause type errors when mapped to SQL datetime fields.

        Args:
            df (pd.DataFrame): DataFrame potentially containing datetime columns.

        Returns:
            pd.DataFrame: The modified DataFrame with datetime columns converted to object type
                        and NaT values replaced by None.
        """
        for col in df.select_dtypes(include=["datetime64[ns]"]):
            df[col] = df[col].astype(object).where(df[col].notna(), None)
        return df     

    def load_to_postgres(self, data_frame: pd.DataFrame, data_model: Type[BaseModel], conflict_keys:list[str]) -> list[dict]:
        """
        Performs an UPSERT (insert or update on conflict) operation into a PostgreSQL database using a generic SQLAlchemy ORM model.

        This function takes a validated Pandera DataFrameModel and attempts to insert each row into the specified table
        represented by the SQLAlchemy model. If a record with the specified conflict keys already exists, it will be updated
        with the new values provided in the DataFrame.

        Args:
            data_frame (pa.DataFrameModel): A validated Pandera DataFrameModel containing the data to be inserted or updated.
            data_model (Type[BaseModel]): A SQLAlchemy ORM model class representing the target database table.
            conflict_keys (list[str]): List of column names that define the uniqueness constraint to detect conflicts during insertion.

        Returns:
            list[dict]: A list of dictionaries representing the rows that were inserted or updated in the database.

        Raises:
            SQLAlchemyError: If any error occurs during the database operation, the transaction is rolled back and the error is re-raised.
        """
        with SessionLocal() as db:
            try:
                rows = cast(list[dict[str, Any]], data_frame.to_dict(orient="records"))

                for row in rows:
                    stmt = insert(data_model).values(**row)

                    # Fields to update if a conflict is detected
                    update_dict = {k: v for k, v in row.items() if k not in conflict_keys}

                    stmt = stmt.on_conflict_do_update(
                        index_elements=conflict_keys,
                        set_=update_dict
                    )

                    db.execute(stmt)
                db.commit()
                return rows
            except SQLAlchemyError as e:
                db.rollback()
                print("Error saving to the database:")
                print(e.__class__.__name__, "-", str(e))
                raise