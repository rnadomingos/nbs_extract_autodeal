import pandas as pd

class FormatColumn:
    def formatDatetime(self, df: pd.DataFrame) -> pd.DataFrame:
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

