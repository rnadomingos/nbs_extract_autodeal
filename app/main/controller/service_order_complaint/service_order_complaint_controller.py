from data.models.service_order_model import ServiceOrderModel
from main.usecases.destination.load_max_date_column import TableTools
from data.models.service_order_complaint_model import ServiceOrderComplaintModel
from main.usecases.source.extract_data import ExtractData
from data.sql.service_orders_complaint import (stmt_open_service_order_complaint, stmt_closed_service_order_complaint)
from data.schemas.service_orders_complaint.service_order_complaint_schema import ServiceOrdersComplaintSchema
from main.usecases.destination.upsert_data import UpsertData

class ServiceOrderComplaintController:

    def open_service_order_complaint_upsert(self):
        max_emission_date = TableTools().loadMaxDateColumn(
            date_column=ServiceOrderModel.data_emissao
        )
        extractData = ExtractData(
            query=stmt_open_service_order_complaint,
            query_params=max_emission_date
        )
        data_frame_service_order_complaint = extractData.get_data_nbs(
            schema=ServiceOrdersComplaintSchema, #type: ignore
            lazy=True
        )
        upsert_service_order_complaint = UpsertData(
            data_frame=data_frame_service_order_complaint,
            data_model=ServiceOrderComplaintModel,
            conflict_keys=['cod_empresa', 'numero_os', 'item']
        )
        saved_service_order_complaints = upsert_service_order_complaint.save_data()
        return len(saved_service_order_complaints)
    
    def closed_service_order_complaint_upsert(self):
        max_closed_date = TableTools().loadMaxDateColumn(
            date_column=ServiceOrderModel.data_encerramento
        )
        extractData = ExtractData(
            query=stmt_closed_service_order_complaint,
            query_params=max_closed_date
        )
        data_frame_service_order_complaint = extractData.get_data_nbs(
            schema=ServiceOrdersComplaintSchema, #type: ignore
            lazy=True
        )
        upsert_service_order_complaint = UpsertData(
            data_frame=data_frame_service_order_complaint,
            data_model=ServiceOrderComplaintModel,
            conflict_keys=['cod_empresa', 'numero_os', 'item']
        )
        saved_service_order_complaints = upsert_service_order_complaint.save_data()
        return len(saved_service_order_complaints)
    