import time

from main.controller.service_orders_cover.service_orders_controller import ServiceOrderController

from extract_stages._log import line, total_atualizados


class ServiceOrdersCoverStage:
    def execute(self) -> None:
        start_time = time.time()

        line("Iniciando o processamento OS Capa.")

        os_capa_controller = ServiceOrderController()

        line("Processando Ordens de Serviço Capa abertas.")
        service_orders_open = os_capa_controller.open_service_orders_upsert()
        total_atualizados("service_orders_open", service_orders_open)

        line("Processando Ordens de Serviço Capa encerradas.")
        service_orders_closed = os_capa_controller.closed_service_orders_upsert()
        total_atualizados("service_orders_closed", service_orders_closed)

        line("Processando Ordens de Serviço Capa Canceladas.")
        service_orders_canceled = os_capa_controller.canceled_service_orders_upsert()
        total_atualizados("service_orders_canceled", service_orders_canceled)

        time.sleep(2)

        end_time = time.time()
        line(f"Processamento concluído em {end_time - start_time:.2f} segundos.")


def build_service_orders_cover() -> ServiceOrdersCoverStage:
    return ServiceOrdersCoverStage()
