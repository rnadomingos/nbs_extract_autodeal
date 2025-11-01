from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import declarative_base
from infra.postgres_database import engine
from datetime import datetime
import pytz

Base = declarative_base()

class RelatedServiceOrderModel(Base):
    """
    Modelo ORM para a tabela OS Relacionadas.
    Attributes:
        cod_empresa (int): Identificador da Empresa.
        numero_os (int): Numero da ordem de serviço.
        numero_os_irma (int): Numero da ordem de serviço irma
    """

    def now_utc_minus_3(self):
        return datetime.now(pytz.timezone("America/Sao_Paulo"))

    __tablename__ = "os_relacionadas"

    id = Column(Integer, primary_key=True, autoincrement=True)

    cod_empresa = Column(Integer, nullable=False)
    numero_os = Column(Integer, nullable=False)
    numero_os_irma = Column(Integer, nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "cod_empresa", 
            "numero_os", 
            "numero_os_irma", 
            name="uq_cod_empresa_numero_os__numero_os_irma"),
    )

Base.metadata.create_all(engine)