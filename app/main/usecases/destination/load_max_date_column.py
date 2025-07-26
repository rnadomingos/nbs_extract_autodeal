from infra.postgres_database import PostgresSessionLocal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from typing import Any
import os

class LoadMaxDateColumn:
    
    def load(self, date_column:Any) -> dict: 
        """
        Get the maximum date from the given model column and format as 'yyyy-MM-dd'.

        Args:
            date_column (Any): A SQLAlchemy model column (e.g., OSCapaModel.data_cadastro).
            
        Returns:
            dict: A dictionary with the max date as 'yyyy-MM-dd', or None if not found.
        """
        START_DATE = os.getenv('INTEGRATION_START_DATE')
        with PostgresSessionLocal() as db:
            try:
                result = db.query(func.max(date_column)).one()
                max_date = result[0]
                db.commit()
                if max_date:
                     return { 'max_date': max_date.strftime('%Y-%m-%d')}
                return { 'max_date': START_DATE }
            except SQLAlchemyError as e:
                db.rollback()
                print("Error load max date:")
                print(e.__class__.__name__, "-", str(e._message))
                raise
        return 
