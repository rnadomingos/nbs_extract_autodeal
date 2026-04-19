from include.data.schemas.service_orders_invoices.service_order_invoice_schema import ServiceOrdersInvoice
from include.data.models.service_orders_invoice_model import ServiceOrdersInvoiceModel
from include.data.models.service_order_model import ServiceOrderModel
from include.data.sql.service_orders_invoices import (
    stmt_closed_service_order_invoices,
    stmt_open_service_order_invoices
)
from include.main.usecases.destination.load_max_date_column import TableTools
from include.main.usecases.source.extract_data import ExtractData
from include.main.usecases.destination.upsert_data import UpsertData

class ServiceOrderInvoicesController:
    def open_service_order_invoices_upsert(self):
        max_emission_date = TableTools().loadMaxDateColumn(
            date_column=ServiceOrderModel.data_emissao
        )
        extractData = ExtractData(
            query=stmt_open_service_order_invoices,
            query_params=max_emission_date
        )
        data_frame_service_order_invoices = extractData.get_data_nbs(
            schema=ServiceOrdersInvoice, #type: ignore
            lazy=True
        )
        upsert_service_order_invoices = UpsertData(
            data_frame=data_frame_service_order_invoices,
            data_model=ServiceOrdersInvoiceModel,
            conflict_keys=['cod_empresa', 'numero_os', 'nr_nota_fiscal']
        )
        saved_service_order_invoices = upsert_service_order_invoices.save_data()
        return len(saved_service_order_invoices)
    
    def closed_service_order_invoices_upsert(self):
        max_closed_date = TableTools().loadMaxDateColumn(
            date_column=ServiceOrderModel.data_encerramento
        )
        extractData = ExtractData(
            query=stmt_closed_service_order_invoices,
            query_params=max_closed_date
        )
        data_frame_service_order_invoices = extractData.get_data_nbs(
            schema=ServiceOrdersInvoice, #type: ignore
            lazy=True
        )
        upsert_service_order_invoices = UpsertData(
            data_frame=data_frame_service_order_invoices,
            data_model=ServiceOrdersInvoiceModel,
            conflict_keys=['cod_empresa', 'numero_os', 'nr_nota_fiscal']
        )
        saved_service_order_invoices = upsert_service_order_invoices.save_data()
        return len(saved_service_order_invoices)
        