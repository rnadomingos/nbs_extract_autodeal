from include.data.sql.related_service_orders.sql_open_related_service_order import stmt_open_related_service_orders
from include.utils.infer_schemas import InferSchema
from include.main.usecases.source.extract_data import ExtractData

def related_service_order_inferSchema():
    data_source_related_service_order = ExtractData(
       query=stmt_open_related_service_orders,
       query_params={ 'max_date': '2025-07-01' }
    )
    data_to_infer = data_source_related_service_order.get_data_infer_schema_nbs()
    path_save_file = 'app/data/schemas/related_service_orders_schema.py'
    inferSchema = InferSchema(data_frame=data_to_infer, path_save_file=path_save_file)
    schema = inferSchema.makeInferSchema()
    return schema



if __name__ == '__main__':
    schema = related_service_order_inferSchema()