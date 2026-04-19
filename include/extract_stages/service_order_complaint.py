from include.main.controller.service_order_complaint.service_order_complaint_controller import (
    ServiceOrderComplaintController,
)

from include.extract_stages._log import line, total


class ServiceOrderComplaintStage:
    def execute(self) -> None:
        line("Iniciando o processamento das reclamações da OS")
        service_order_complaint_controller = ServiceOrderComplaintController()

        line("Processando Reclamações de Ordens de Serviço abertas.")
        service_order_complaint_open = service_order_complaint_controller.open_service_order_complaint_upsert()
        total("service_order_complaint_open", service_order_complaint_open)

        line("Processando Reclamações de Ordens de Serviço encerradas.")
        service_order_complaint_closed = service_order_complaint_controller.closed_service_order_complaint_upsert()
        total("service_order_complaint_closed", service_order_complaint_closed)


def build_service_order_complaint() -> ServiceOrderComplaintStage:
    return ServiceOrderComplaintStage()
