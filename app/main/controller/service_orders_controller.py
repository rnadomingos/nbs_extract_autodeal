from main.usecases.destination.load_max_date_column import LoadMaxDateColumn
from main.usecases.transformation.format_column import FormatColumn
from main.usecases.destination.upsert_data import UpsertData
from main.usecases.source.extract_data import ExtractData
from data.models.service_order_model import ServiceOrderModel
from data.schemas.os_capa_schema import OSCapaSchema
from data.sql.service_orders import (stmt_open_service_orders,
                                         stmt_closed_service_orders,
                                         stmt_canceled_service_orders)


class ServiceOrderController:
    def open_service_orders_upsert(self):
        
        max_emission_date = LoadMaxDateColumn().load(
            date_column=ServiceOrderModel.data_emissao
            )
        extractData = ExtractData(
            query=stmt_open_service_orders, 
            query_params=max_emission_date,
            
            )
        data_frame_os_capa = extractData.get_data_nbs(
            schema=OSCapaSchema, #type: ignore
            lazy=True)
        data_frame_os_capa = FormatColumn().formatDatetime(
            df=data_frame_os_capa
            )
        upsert_os_capa = UpsertData(
            data_frame=data_frame_os_capa,
            data_model=ServiceOrderModel,
            conflict_keys=['cod_empresa', 'numero_os']
        )
        saved_os_capa = upsert_os_capa.save_data()
        return len(saved_os_capa)
    
    def closed_service_orders_upsert(self):
        
        max_closed_date = LoadMaxDateColumn().load(
            date_column=ServiceOrderModel.data_encerramento
            )
        extractData = ExtractData(
            query=stmt_closed_service_orders, 
            query_params=max_closed_date,
            
            )
        data_frame_os_capa = extractData.get_data_nbs(
            schema=OSCapaSchema, #type: ignore
            lazy=True
        )
        data_frame_os_capa = FormatColumn().formatDatetime(
            df=data_frame_os_capa
            )
        upsert_os_capa = UpsertData(
            data_frame=data_frame_os_capa,
            data_model=ServiceOrderModel,
            conflict_keys=['cod_empresa', 'numero_os']
        )
        saved_os_capa = upsert_os_capa.save_data()
        return len(saved_os_capa)
    
    def canceled_service_orders_upsert(self):
        
        max_date_cancellation = LoadMaxDateColumn().load(
            date_column=ServiceOrderModel.data_cancelamento
            )
        extractData = ExtractData(
            query=stmt_canceled_service_orders, 
            query_params=max_date_cancellation,
            )
        data_frame_os_capa = extractData.get_data_nbs(
            schema=OSCapaSchema, #type: ignore
            lazy=True)
        data_frame_os_capa = FormatColumn().formatDatetime(
            df=data_frame_os_capa
            )
        upsert_os_capa = UpsertData(
            data_frame=data_frame_os_capa,
            data_model=ServiceOrderModel,
            conflict_keys=['cod_empresa', 'numero_os']
        )
        saved_os_capa = upsert_os_capa.save_data()
        return len(saved_os_capa)