from include.main.controller.service_order_services.service_order_services_controller import (
    ServiceOrderServicesController,
)

from include.extract_stages._log import line, total


class ServiceOrderServicesStage:    
    def execute(self) -> None:
        line("Iniciando o processamento dos serviços da OS")
        service_order_services_controller = ServiceOrderServicesController()

        line("Processando Serviços de Ordens de Serviço abertas.")
        service_order_services_open = service_order_services_controller.open_service_order_services_upsert()
        total("service_order_services_open", service_order_services_open)

        line("Processando Serviços de Ordens de Serviço encerradas.")
        service_order_services_closed = service_order_services_controller.closed_service_order_services_upsert()
        total("service_order_services_closed", service_order_services_closed)


def build_service_order_services() -> ServiceOrderServicesStage:
    return ServiceOrderServicesStage()
