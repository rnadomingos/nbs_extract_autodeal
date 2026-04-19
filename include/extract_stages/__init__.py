"""Orquestração da extração: satélites antes da capa da OS."""

from .customer_service_orders import build_customer_service_orders
from .items_service_orders import build_items_service_orders
from .related_service_orders import build_related_service_orders
from .service_order_complaint import build_service_order_complaint
from .service_order_services import build_service_order_services
from .service_order_invoices import build_service_order_invoices
from .service_orders_cover import build_service_orders_cover

def run() -> None:
    """Executa as etapas na ordem exigida pelo modelo de dados.

    Importar primeiro as tabelas satélites (clientes, OS relacionadas, itens,
    serviços, reclamações) e por último a OS capa: a maior data no Autodeal
    para satélites depende de não ter importado só a capa antes.
    """
    build_customer_service_orders().execute()
    build_related_service_orders().execute()
    build_items_service_orders().execute()
    build_service_order_services().execute()
    build_service_order_complaint().execute()
    build_service_order_invoices().execute()
    build_service_orders_cover().execute()