from main.usecases.destination.load_max_date_column import LoadMaxDateColumn
from data.models.customer_service_order_model import CustomerServiceOrderModel
from data.models.service_order_model import ServiceOrderModel
from main.usecases.source.extract_data import ExtractData
from data.sql.customer_service_orders import (stmt_open_customer_service_orders, stmt_closed_customers_service_order)
from data.schemas.customer_service_order_schema import CustomerServiceOrderSchema
from main.usecases.destination.upsert_data import UpsertData

class CustomerServiceOrderController:
    def open_customer_service_order_upsert(self):
        
        max_emission_date = LoadMaxDateColumn().load(
            date_column=ServiceOrderModel.data_emissao
        )

        extractData = ExtractData(
            query=stmt_open_customer_service_orders,
            query_params={ 'max_date': '2025-07-01' }
        )

        data_frame_customer_service_order = extractData.get_data_nbs(
            schema=CustomerServiceOrderSchema, #type: ignore
            lazy=True
        )
        upsert_customer_service_order = UpsertData(
            data_frame=data_frame_customer_service_order,
            data_model=CustomerServiceOrderModel,
            conflict_keys=['cod_empresa', 'numero_os']
        )
        saved_customers_service_order = upsert_customer_service_order.save_data()
        return len(saved_customers_service_order)
    
    def closed_customer_service_order_upsert(self):
        max_closed_date = LoadMaxDateColumn().load(
            date_column=ServiceOrderModel.data_encerramento
        )

        extractData = ExtractData(
            query=stmt_closed_customers_service_order,
            query_params={ 'max_date': '2025-07-01' }
        )

        data_frame_customer_service_order = extractData.get_data_nbs(
            schema=CustomerServiceOrderSchema, #type: ignore
            lazy=True
        )
        upsert_customer_service_order = UpsertData(
            data_frame=data_frame_customer_service_order,
            data_model=CustomerServiceOrderModel,
            conflict_keys=['cod_empresa', 'numero_os']
        )
        saved_customers_service_order = upsert_customer_service_order.save_data()
        return len(saved_customers_service_order)