import time

from include.main.controller.customer_service_orders.customer_service_orders_controller import (
    CustomerServiceOrderController,
)

from include.extract_stages._log import line, total_atualizados


class CustomerServiceOrdersStage:
    def execute(self) -> None:
        line("Iniciando o processamento OS Capa Cliente.")
        customer_service_order = CustomerServiceOrderController()

        line("Processando Clientes de Ordens de Serviço Capa abertas.")
        open_customer_service_order = customer_service_order.open_customer_service_order_upsert()
        total_atualizados("customer_service_orders_open", open_customer_service_order)

        line("Processando Clientes de Ordens de Serviço Capa encerradas.")
        closed_customer_service_order = customer_service_order.closed_customer_service_order_upsert()
        total_atualizados("customer_service_orders_closed", closed_customer_service_order)

        time.sleep(2)


def build_customer_service_orders() -> CustomerServiceOrdersStage:
    return CustomerServiceOrdersStage()
