from include.main.controller.related_service_orders.related_service_orders_controller import (
    RelatedServiceOrderController,
)

from include.extract_stages._log import line, total


class RelatedServiceOrdersStage:
    def execute(self) -> None:
        line("Iniciando o processamento OS Relacionada")
        related_service_order_controller = RelatedServiceOrderController()

        line("Processando Ordens de Serviço Relacionadas abertas.")
        related_service_order_open = related_service_order_controller.open_related_service_order_upsert()
        total("related_service_order_open", related_service_order_open)

        line("Processando Ordens de Serviço Relacionadas encerradas.")
        related_service_order_closed = related_service_order_controller.closed_related_service_order_upsert()
        total("related_service_order_closed", related_service_order_closed)


def build_related_service_orders() -> RelatedServiceOrdersStage:
    return RelatedServiceOrdersStage()
