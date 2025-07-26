from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, UniqueConstraint
from sqlalchemy.orm import declarative_base
from infra.postgres_database import engine
from datetime import datetime
import pytz

Base = declarative_base()

class OSCapaModel(Base):
    """
    Modelo ORM para a tabela da OS Capa.
    Attributes:
        cod_empresa (int): Identificador da Empresa (entre 2 e 3).
        numero_os (int): Número da ordem de serviço.
        data_emissao (datetime): Data de emissão da OS.
        data_encerramento (str): Data de encerramento da OS.
        data_cancelamento (str): Data de cancelamento da OS.
        ...
    """
    def now_utc_minus_3(self):
        return datetime.now(pytz.timezone("America/Sao_Paulo"))

    __tablename__ = "os_capa"

    id = Column(Integer, primary_key=True, autoincrement=True)  # campo auxiliar

    cod_empresa = Column(Integer, nullable=False)
    numero_os = Column(Integer, nullable=False)
    os_original = Column(String, nullable=False)
    data_emissao = Column(DateTime, nullable=False)
    data_encerramento = Column(String, nullable=True)
    data_cancelamento = Column(String, nullable=True)
    razao_social = Column(String, nullable=False)
    tipo_os = Column(String, nullable=False)
    responsavel = Column(String, nullable=False)
    chassi = Column(String, nullable=False)
    veic_modelo = Column(String, nullable=False)
    ano = Column(String, nullable=False)
    km = Column(Integer, nullable=False)
    placa = Column(String, nullable=True)
    data_venda = Column(DateTime, nullable=True)
    status_os = Column(String, nullable=False)
    numero_do_dealer = Column(String, nullable=False)
    razao_social_dealer = Column(String, nullable=False)
    valor_estimado_os = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), default=now_utc_minus_3)
    updated_at = Column(DateTime(timezone=True), default=now_utc_minus_3, onupdate=now_utc_minus_3)
    sent_autodeal = Column(Boolean, default=False)
    sent_at_autodeal = Column(DateTime(timezone=True), nullable=True)
    updated_at_autodeal = Column(DateTime(timezone=True), nullable=True)
    
    __table_args__ = (
        UniqueConstraint("cod_empresa", "numero_os", name="uq_cod_empresa_numero_os"),
    )

Base.metadata.create_all(engine)