from main.usecases.destination.load_max_date_column import TableTools
from main.usecases.source.extract_data import ExtractData
from main.usecases.destination.upsert_data import UpsertData
from data.models.related_service_order_model import RelatedServiceOrderModel
from data.models.service_order_model import ServiceOrderModel
from data.schemas.related_service_orders.related_service_orders_schema import RelatedServiceOrderSchema
from main.usecases.transformation.format_column import FormatColumn
from data.sql.related_service_orders import (
    stmt_closed_related_service_orders, 
    stmt_open_related_service_orders
    )
import os

class RelatedServiceOrderController:
    def open_related_service_order_upsert(self):
        
        max_emission_date = TableTools().loadMaxDateColumn(
            date_column=ServiceOrderModel.data_emissao
            )

        extractData = ExtractData(
            query=stmt_open_related_service_orders,
            query_params= max_emission_date
        )

        data_frame_related_service_order = extractData.get_data_nbs(
            schema=RelatedServiceOrderSchema, #type: ignore
            lazy=True
        )

        upsert_related_service_order = UpsertData(
            data_frame=data_frame_related_service_order,
            data_model=RelatedServiceOrderModel,
            conflict_keys=['cod_empresa', 'numero_os', 'numero_os_irma'],
        )

        saved_related_service_order = upsert_related_service_order.save_data()
        return len(saved_related_service_order)
    
    def closed_related_service_order_upsert(self):
        
        max_closed_date = TableTools().loadMaxDateColumn(
            date_column=ServiceOrderModel.data_encerramento
            )

        extractData = ExtractData(
            query=stmt_closed_related_service_orders,
            query_params= max_closed_date
        )

        data_frame_related_service_order = extractData.get_data_nbs(
            schema=RelatedServiceOrderSchema, #type: ignore
            lazy=True
        )

        upsert_related_service_order = UpsertData(
            data_frame=data_frame_related_service_order,
            data_model=RelatedServiceOrderModel,
            conflict_keys=['cod_empresa', 'numero_os', 'numero_os_irma'],
        )

        saved_related_service_order = upsert_related_service_order.save_data()
        return len(saved_related_service_order)