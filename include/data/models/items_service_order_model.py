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
        item (int): Item da ordem de serviço.
        cod_servico (str): Código do serviço associado.
        cod_item (str): Código do item/peça.
        descricao (str): Descrição do item/peça.
        qtde_peca (int): Quantidade de peças na ordem de serviço.
        valor_os (Numeric): Valor do item na ordem de serviço.
    """

    def now_utc_minus_3(self):
        return datetime.now(pytz.timezone("America/Sao_Paulo"))

    __tablename__ = "itens_ordem_servico"

    id = Column(Integer, primary_key=True, autoincrement=True)

    cod_empresa = Column(Integer, nullable=False)
    numero_os = Column(Integer, nullable=False)
    item = Column(Integer, nullable=True)
    cod_servico = Column(String, nullable=True)
    cod_item = Column(String, nullable=True)
    descricao = Column(String, nullable=True)
    qtde_peca = Column(Integer, nullable=True)
    valor_os = Column(Numeric(10, 2), nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "cod_empresa",
            "numero_os",
            "item",
            "cod_item",
            name="uq_cod_empresa_numero_os_item_cod_item",
        ),
    )


Base.metadata.create_all(engine)
