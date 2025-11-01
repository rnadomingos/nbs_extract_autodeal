from main.controller.service_orders.service_orders_controller import ServiceOrderController
from main.controller.customer_service_orders.customer_service_orders_controller import CustomerServiceOrderController
from main.controller.related_service_orders.related_service_orders_controller import RelatedServiceOrderController
import time



if __name__ == "__main__":

    """
    É preciso iniciar a importação dos dados das tabelas satélites 
    como clientes, OS relacionadas, item e serviços e 
    posteriormente a da OS capa que é a principal.

    Deve ser assim, porque para fazer a importação das tabelas satélites 
    eu verifico a maior data na base de dados do Autodeal 
    considero a importação a partir dele.

    Se importar primeiro a OS Capa, quando eu verificar a maior data para 
    importar as tabelas satélites, perderemos informações.
    """

    print(f"Iniciando o processamento OS Capa Cliente.")
    customer_service_order = CustomerServiceOrderController()

    print(f"Processando Clientes de Ordens de Serviço Capa abertas.")
    open_customer_service_order = customer_service_order.open_customer_service_order_upsert()
    print(f'Total de registros customer_service_orders_open atualizados: {open_customer_service_order}')
    
    print(f"Processando Clientes de Ordens de Serviço Capa encerradas.")
    closed_customer_service_order = customer_service_order.closed_customer_service_order_upsert()
    print(f'Total de registros customer_service_orders_closed atualizados: {closed_customer_service_order}')

    time.sleep(2)

    print("Iniciando o processamento OS Relacionada")
    related_service_order_controller = RelatedServiceOrderController()
    
    print(f"Processando Ordens de Serviço Relacionadas abertas.")
    related_service_order_open = related_service_order_controller.open_related_service_order_upsert()
    print(f"Total de registros related_service_order_open: {related_service_order_open}")
    
    print(f"Processando Ordens de Serviço Relacionadas encerradas.")
    related_service_order_closed = related_service_order_controller.closed_related_service_order_upsert
    print(f"Total de registros related_service_order_closed: {related_service_order_closed}")
    
    print(f"Iniciando o processamento OS Capa.")
    start_time = time.time()
    os_capa_controller = ServiceOrderController()
    print(f"Processando Ordens de Serviço Capa abertas.")
    service_orders_open = os_capa_controller.open_service_orders_upsert()
    print(f'Total de registros service_orders_open atualizados: {service_orders_open}')
    
    print(f"Processando Ordens de Serviço Capa encerradas.")
    service_orders_closed = os_capa_controller.closed_service_orders_upsert()
    print(f'Total de registros service_orders_closed atualizados: {service_orders_closed}')
    
    print(f"Processando Ordens de Serviço Capa Canceladas.")
    service_orders_canceled = os_capa_controller.canceled_service_orders_upsert()
    print(f'Total de registros service_orders_canceled atualizados: {service_orders_canceled}')

    time.sleep(2)
    
    
    end_time = time.time()
    print(f"Processamento concluído em {end_time-start_time:.2f} segundos.")
    
