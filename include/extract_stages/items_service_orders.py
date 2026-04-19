from include.main.controller.items_service_orders.items_service_orders_controller import (
    ItemsServiceOrdersController,
)

from include.extract_stages._log import line, total


class ItemsServiceOrdersStage:
    def execute(self) -> None:
        line("Iniciando o processamento dos itens da OS")
        items_service_orders_controller = ItemsServiceOrdersController()

        line("Processando Itens de Ordens de Serviço abertas.")
        items_service_orders_open = items_service_orders_controller.open_items_service_order_upsert()
        total("items_service_orders_open", items_service_orders_open)

        line("Processando Itens de Ordens de Serviço encerradas.")
        items_service_orders_closed = items_service_orders_controller.closed_items_service_order_upsert()
        total("items_service_orders_closed", items_service_orders_closed)


def build_items_service_orders() -> ItemsServiceOrdersStage:
    return ItemsServiceOrdersStage()
