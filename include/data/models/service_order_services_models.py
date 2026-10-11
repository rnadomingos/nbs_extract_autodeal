from sqlalchemy import Column, Integer, String, UniqueConstraint, Numeric
from sqlalchemy.orm import declarative_base
from include.infra.postgres_database import engine
from datetime import datetime
import pytz

Base = declarative_base()

class ServiceOrderServicesModel(Base):
    """
    Modelo ORM para a tabela Serviços da Ordem de Serviço.
    Attributes:
        cod_empresa (int): Identificador da Empresa.
        numero_os (int): Numero da ordem de serviço.
        item (int): Item/número de sequência do serviço.
        codigo_servico (str): Código do serviço realizado.
        cod_defeito (str): Código do defeito associado.
        descritivo (str): Descrição do serviço.
        valor (Numeric): Valor da mão de obra na OS.
    """

    def now_utc_minus_3(self):
        return datetime.now(pytz.timezone("America/Sao_Paulo"))

    __tablename__ = "servicos_ordem_servico"

    id = Column(Integer, primary_key=True, autoincrement=True)

    cod_empresa = Column(Integer, nullable=False)
    numero_os = Column(Integer, nullable=False)
    item = Column(Integer, nullable=True)
    codigo_servico = Column(String, nullable=True)
    cod_defeito = Column(String, nullable=True)
    descritivo = Column(String, nullable=True)
    valor = Column(Numeric(10, 2), nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "cod_empresa",
            "numero_os",
            "item",
            "codigo_servico",
            name="uq_cod_empresa_numero_os_item_codigo_servico"),
    )

Base.metadata.create_all(engine)