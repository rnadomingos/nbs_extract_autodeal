from sqlalchemy import Column, DateTime, Float, Integer, String, UniqueConstraint
from sqlalchemy.orm import declarative_base
from infra.postgres_database import engine


Base = declarative_base()

class ServiceOrdersInvoiceModel(Base):
    """
    Modelo ORM para a tabela de Faturas de Ordens de Serviço.
    Attributes:
        cod_empresa (int): Identificador da Empresa.
        numero_os (int): Numero da ordem de serviço.
        nr_sg (str): Número de série do equipamento.
        tipo_nota_fiscal (str): Tipo da nota fiscal.
        nr_nota_fiscal (int): Numero da nota fiscal.
        data_referencia (datetime): Data de referência da fatura.
        valor (float): Valor da fatura.
    """

    __tablename__ = "notas_fiscais_ordem_servico"

    id = Column(Integer, primary_key=True, autoincrement=True)

    cod_empresa = Column(Integer, nullable=False)
    numero_os = Column(Integer, nullable=False)
    nr_sg = Column(String, nullable=True)
    tipo_nota_fiscal = Column(String, nullable=False)
    nr_nota_fiscal = Column(Integer, nullable=True)
    data_referencia = Column(DateTime, nullable=True)
    valor = Column(Float, nullable=True)

    __table_args__ = (
        UniqueConstraint(
            'cod_empresa', 
            'numero_os', 
            name='uq_service_order_invoice'),
    )


Base.metadata.create_all(engine)