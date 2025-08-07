from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import declarative_base
from infra.postgres_database import engine
from datetime import datetime
import pytz

Base = declarative_base()

class CustomerServiceOrderModel(Base):
    """
    Modelo ORM para a tabela da OS Capa.
    Attributes:
        cod_empresa (int): Identificador da Empresa.
        numero_os (int): Numero da ordem de serviço.
        nome_cliente(str): Nome do cliente da orde de serviço.
        cpf_cnpj(str): CPF ou CNPJ.
        telefone (str): Telefone do cliente.
        celular (str): Celular do cliente.
    """

    def now_utc_minus_3(self):
        return datetime.now(pytz.timezone("America/Sao_Paulo"))

    __tablename__ = "os_clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)

    cod_empresa = Column(Integer, nullable=False)
    numero_os = Column(Integer, nullable=False)
    nome_cliente = Column(String, nullable=False)
    cpf_cnpj = Column(String, nullable=False)
    telefone = Column(String, nullable=True)
    celular =  Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=now_utc_minus_3)
    updated_at = Column(DateTime(timezone=True), default=now_utc_minus_3, onupdate=now_utc_minus_3)

    __table_args__ = (
        UniqueConstraint("cod_empresa", "numero_os", name="uq_cod_empresa_numero_os_clientes"),
    )

Base.metadata.create_all(engine)