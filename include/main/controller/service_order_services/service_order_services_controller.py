from include.data.schemas.service_order_services.service_order_services_schema import ServiceOrderServicesSchema
from include.main.usecases.destination.load_max_date_column import TableTools
from include.data.models.service_order_model import ServiceOrderModel
from include.data.models.service_order_services_models import ServiceOrderServicesModel
from include.main.usecases.source.extract_data import ExtractData
from include.data.sql.service_order_services.sql_open_service_order_services import stmt_open_service_order_services
from include.data.sql.service_order_services.sql_closed_service_order_services import stmt_closed_service_order_services
from include.main.usecases.destination.upsert_data import UpsertData

class ServiceOrderServicesController:
    """
    Controlador para o processamento dos Serviços das Ordens de Serviço.
    
    A ordem de processamento das tabelas de Ordens de Serviço é crítica.
    Ao invés de importar Primeiro a tabela de OS Capa, faço ela por último para verificar primeiro qual é a última data importada e fazer a importação das tabelas satélites (clientes, OS relacionadas, itens e serviços)
    eu verifico a maior data na tabela de OS Capa do Autodeal e considero a importação a partir dele.
    Se importar primeiro a OS Capa, quando eu verificar a maior data para importar as tabelas satélites, perderemos informações.
    """

    def open_service_order_services_upsert(self):
        max_emission_date = TableTools().loadMaxDateColumn(
            date_column=ServiceOrderModel.data_emissao
        )
        extractData = ExtractData(
            query=stmt_open_service_order_services,
            query_params=max_emission_date
        )
        data_frame_service_order_services = extractData.get_data_nbs(
            schema=ServiceOrderServicesSchema, #type: ignore
            lazy=True
        )
        upsert_service_order_services = UpsertData(
            data_frame=data_frame_service_order_services,
            data_model=ServiceOrderServicesModel,
            conflict_keys=['cod_empresa', 'numero_os', 'codigo_servico']
        )   
        saved_service_order_services = upsert_service_order_services.save_data()
        return len(saved_service_order_services)    

    def closed_service_order_services_upsert(self):
        max_closed_date = TableTools().loadMaxDateColumn(
            date_column=ServiceOrderModel.data_encerramento
        )
        extractData = ExtractData(
            query=stmt_closed_service_order_services,
            query_params=max_closed_date
        )
        data_frame_service_order_services = extractData.get_data_nbs(
            schema=ServiceOrderServicesSchema, #type: ignore
            lazy=True
        )
        upsert_service_order_services = UpsertData(
            data_frame=data_frame_service_order_services,
            data_model=ServiceOrderServicesModel,
            conflict_keys=['cod_empresa', 'numero_os', 'codigo_servico']
        )   
        saved_service_order_services = upsert_service_order_services.save_data()
        return len(saved_service_order_services)