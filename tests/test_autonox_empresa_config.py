import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from include.data.models.autonox_empresa_config_model import AutonoxEmpresaConfigModel, Base
from include.data.seeds.empresa_config_seed import seed_empresa_config, INITIAL_EMPRESA_SEEDS
from include.clients.autonox_client import AutonoxHttpClient
from include.services.sync_service import SyncService


@pytest.fixture
def memory_db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


def test_autonox_empresa_config_model_creation(memory_db):
    Session = sessionmaker(bind=memory_db)
    session = Session()

    config = AutonoxEmpresaConfigModel(
        codigo_empresa=10,
        sigla="TST",
        marca="BMW",
        api_key="secret_test_key",
        is_active=True
    )
    session.add(config)
    session.commit()

    retrieved = session.query(AutonoxEmpresaConfigModel).filter_by(codigo_empresa=10).first()
    assert retrieved is not None
    assert retrieved.sigla == "TST"
    assert retrieved.marca == "BMW"
    assert retrieved.api_key == "secret_test_key"
    assert retrieved.is_active is True


def test_seed_empresa_config(memory_db):
    inserted_count = seed_empresa_config(memory_db)
    assert inserted_count >= len(INITIAL_EMPRESA_SEEDS)

    Session = sessionmaker(bind=memory_db)
    session = Session()

    emp2 = session.query(AutonoxEmpresaConfigModel).filter_by(codigo_empresa=2).first()
    assert emp2 is not None
    assert emp2.sigla == "GPBB"
    assert emp2.is_active is True
    assert emp2.api_key != ""


def test_autonox_client_empresa_api_key():
    client = AutonoxHttpClient(api_url="http://mock-endpoint")
    
    # Test send_os with specific api_key (without real HTTP call by validating failure key handling or monkeypatch)
    success, status_code, resp_json, err_msg = client.send_os({"numero_os": "123"}, api_key=None)
    # When api_key is None and env has no default, should fail with 401
    assert success is False
    assert status_code == 401
    assert "AUTONOX_API_KEY não informada" in err_msg


def test_sync_service_empresa_config_fetching(memory_db):
    seed_empresa_config(memory_db)
    service = SyncService(db_engine=memory_db)

    configs = service.get_empresa_configs()
    assert 2 in configs
    assert configs[2]["sigla"] == "GPBB"
