from infra.postgres_database import PostgresSessionLocal
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from typing import Type, TypeVar, Any, cast
import pandas as pd

Base = declarative_base()

#TypeVar to data_model
BaseModel = TypeVar("T", bound=Base)  # type: ignore

class UpsertData: 
    def __init__(
            self,
            data_frame: pd.DataFrame,
            data_model: Type[BaseModel],
            conflict_keys:list[str]
            ) -> None:
        self.data_frame = data_frame
        self.data_model = data_model
        self.conflict_keys = conflict_keys
        
    def save_data(self) -> list[dict]:
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
        with PostgresSessionLocal() as db:
            try:
                rows = cast(list[dict[str, Any]], self.data_frame.to_dict(orient="records"))

                for row in rows:
                    stmt = insert(self.data_model).values(**row)

                    # Fields to update if a conflict is detected
                    update_dict = {k: v for k, v in row.items() if k not in self.conflict_keys}

                    stmt = stmt.on_conflict_do_update(
                        index_elements=self.conflict_keys,
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