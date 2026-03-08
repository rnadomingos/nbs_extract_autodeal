from data.models.items_service_order_model import ItemsServiceOrderModel
from main.usecases.destination.load_max_date_column import TableTools
from data.models.service_order_model import ServiceOrderModel
from main.usecases.source.extract_data import ExtractData
from data.sql.items_service_orders import (stmt_open_items_service_orders, stmt_closed_items_service_orders)
from data.schemas.items_service_orders.items_service_orders_schema import ItemsServiceOrderSchema 
from main.usecases.destination.upsert_data import UpsertData


class ItemsServiceOrdersController:
    """
    Controlador para o processamento dos Itens das Ordens de Serviço.
    
    A ordem de processamento das tabelas de Ordens de Serviço é crítica.
    Ao invés de importar Primeiro a tabela de OS Capa, faço ela por último para verificar primeiro qual é a última data importada e fazer a importação das tabelas satélites (clientes, OS relacionadas, itens e serviços)
    eu verifico a maior data na tabela de OS Capa do Autodeal e considero a importação a partir dele.
    Se importar primeiro a OS Capa, quando eu verificar a maior data para importar as tabelas satélites, perderemos informações.
    """

    def open_items_service_order_upsert(self):
        max_emission_date = TableTools().loadMaxDateColumn(
            date_column=ServiceOrderModel.data_emissao
            )
        extractData = ExtractData(
            query=stmt_open_items_service_orders,
            query_params=max_emission_date
        )
        data_frame_items_service_order = extractData.get_data_nbs(
            schema=ItemsServiceOrderSchema, #type: ignore
            lazy=True
        )
        upsert_items_service_order = UpsertData(
            data_frame=data_frame_items_service_order,
            data_model=ItemsServiceOrderModel,
            conflict_keys=['cod_empresa', 'numero_os', 'cod_item']
        )
        saved_items_service_orders = upsert_items_service_order.save_data()
        return len(saved_items_service_orders)
    
    def closed_items_service_order_upsert(self):
        max_closed_date = TableTools().loadMaxDateColumn(
            date_column=ServiceOrderModel.data_encerramento
            )
        extractData = ExtractData(
            query=stmt_closed_items_service_orders,
            query_params=max_closed_date
        )
        data_frame_items_service_order = extractData.get_data_nbs(
            schema=ItemsServiceOrderSchema, #type: ignore
            lazy=True
        )
        upsert_items_service_order = UpsertData(
            data_frame=data_frame_items_service_order,
            data_model=ItemsServiceOrderModel,
            conflict_keys=['cod_empresa', 'numero_os', 'cod_item']
        )
        saved_items_service_orders = upsert_items_service_order.save_data()
        return len(saved_items_service_orders)  