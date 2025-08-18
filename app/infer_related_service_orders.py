from main.usecases.source.extract_data import ExtractData
from data.sql.related_service_orders.sql_open_related_service_order import stmt_open_related_service_orders
from utils.infer_schemas import InferSchema


if __name__ == '__main__':

  file_path = 'app/data/schemas/related_service_orders_schema.py'
  
  data_related_service_order = ExtractData(query=stmt_open_related_service_orders, query_params={ 'max_date': '2025-07-01' } )
  df_rso = data_related_service_order.get_data_infer_schema_nbs()
  infer_os_related_service_order = InferSchema(df_rso, file_path)
  infer_os_related_service_order.makeInferSchema()