from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, Numeric
from sqlalchemy.orm import declarative_base
from include.infra.postgres_database import engine
from datetime import datetime
import pytz

Base = declarative_base()

class ItemsServiceOrderModel(Base):
    """
    Modelo ORM para a tabela Itens da Ordem de Serviço.
    Attributes:
        cod_empresa (int): Identificador da Empresa.
        numero_os (int): Numero da ordem de serviço.
        item_os (int): Item da ordem de serviço.
    """

    def now_utc_minus_3(self):
        return datetime.now(pytz.timezone("America/Sao_Paulo"))

    __tablename__ = "itens_ordem_servico"

    id = Column(Integer, primary_key=True, autoincrement=True)

    cod_empresa = Column(Integer, nullable=False)
    numero_os = Column(Integer, nullable=False)
    cod_item = Column(String, nullable=False)
    cod_defeito = Column(String, nullable=True)
    descricao_defeito = Column(String, nullable=True)
    valor_os = Column(Numeric(10, 2), nullable=True)
    valor_oc = Column(Numeric(10, 2), nullable=True)
    quantidade_oc = Column(Integer, nullable=True)
    nr_sg = Column(String, nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "cod_empresa", 
            "numero_os", 
            "cod_item", 
            name="uq_cod_empresa_numero_os_item_os"),
    )

Base.metadata.create_all(engine)  