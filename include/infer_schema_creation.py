## Add sql to import data and infer schema
from include.data.sql.service_orders_invoices.sql_closed_service_order_invoices import stmt_closed_service_order_invoices
from include.utils.infer_schemas import InferSchema
from include.main.usecases.source.extract_data import ExtractData




def infer_schema_creation():
    data_source_schema = ExtractData(
        query=stmt_closed_service_order_invoices,
        ## Add query params if needed, for example, if you want to infer the schema based on a specific date range, you can add it here
        query_params={ "max_date" : "2026-01-01" }   
    )
    data_to_infer = data_source_schema.get_data_infer_schema_nbs()
    ## Add path to save the inferred schema
    path_save_file = 'app/data/schemas/service_orders_invoices/service_order_invoices_schema_inferred.py'
    inferSchema = InferSchema(data_frame=data_to_infer, path_save_file=path_save_file)
    schema = inferSchema.makeInferSchema()
    return schema


if __name__ == "__main__":
    schema = infer_schema_creation()