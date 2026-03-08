from data.sql.items_service_orders.sql_open_items_service_orders import stmt_open_items_service_orders
from utils.infer_schemas import InferSchema
from main.usecases.source.extract_data import ExtractData

def items_service_orders_inferSchema():
    data_source_items_service_orders = ExtractData(
        query=stmt_open_items_service_orders,
        query_params={ "max_date" : "2025-07-01" }   
    )
    data_to_infer = data_source_items_service_orders.get_data_infer_schema_nbs()
    path_save_file = 'app/data/schemas/items_service_orders/items_service_order_schema_inferred.py'
    inferSchema = InferSchema(data_frame=data_to_infer, path_save_file=path_save_file)
    schema = inferSchema.makeInferSchema()
    return schema


if __name__ == "__main__":
    schema = items_service_orders_inferSchema()