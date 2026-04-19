from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import declarative_base
from include.infra.postgres_database import engine
from datetime import datetime
import pytz

Base = declarative_base()

class ServiceOrderComplaintModel(Base):
    """
    Modelo ORM para a tabela Itens da Ordem de Serviço.
    Attributes:
        cod_empresa (int): Identificador da Empresa.
        numero_os (int): Numero da ordem de serviço.
        item_os (int): Item da ordem de serviço.
    """

    def now_utc_minus_3(self):
        return datetime.now(pytz.timezone("America/Sao_Paulo"))

    __tablename__ = "reclamacoes_ordem_servico"

    id = Column(Integer, primary_key=True, autoincrement=True)

    cod_empresa = Column(Integer, nullable=False)
    numero_os = Column(Integer, nullable=False)
    reclamacao = Column(String, nullable=False)
    item = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "cod_empresa", 
            "numero_os", 
            "item", 
            name="uq_cod_empresa_numero_os_item"),
    )

Base.metadata.create_all(engine)  