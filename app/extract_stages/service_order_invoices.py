from main.controller.service_orders_invoice.service_order_invoices_controller import (
    ServiceOrderInvoicesController,
)

from extract_stages._log import line, total_atualizados


class ServiceOrderInvoicesStage:
    def execute(self) -> None:
        line("Iniciando o processamento Notas Fiscais de Ordens de Serviço.")
        service_order_invoice_controller = ServiceOrderInvoicesController()

        line("Processando Notas Fiscais de Ordens de Serviço abertas.")
        service_order_invoice_open = service_order_invoice_controller.open_service_order_invoices_upsert()
        total_atualizados("service_order_invoice_open", service_order_invoice_open)

        line("Processando Notas Fiscais de Ordens de Serviço encerradas.")
        service_order_invoices_closed = service_order_invoice_controller.closed_service_order_invoices_upsert()
        total_atualizados("service_order_invoices_closed", service_order_invoices_closed)


def build_service_order_invoices() -> ServiceOrderInvoicesStage:
    return ServiceOrderInvoicesStage()