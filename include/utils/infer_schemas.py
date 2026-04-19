import pandera.pandas as pa
import pandas as pd

class InferSchema:
    def __init__(
          self,
          data_frame: pd.DataFrame,
          path_save_file: str
        ) -> None:
      self.data_frame = data_frame
      self.path_save_file = path_save_file
    
    def makeInferSchema(self) -> pa.DataFrameSchema:
        path_schema = self.path_save_file # Example: 'app/data/schemas/nome_arquivo.py'
        schema = pa.infer_schema(self.data_frame)
        with open(f'{path_schema}', 'w', encoding='utf-8') as file:
           file.write(str(schema.to_script()))
        
        return schema

