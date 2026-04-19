import oracledb
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from include.infra.load_settings import env_settings

database = 'ORACLE'

load = env_settings(database)
settings = load.load_settings()
oracledb.init_oracle_client(lib_dir=f"{settings['db_driver']}")

ORACLE_STRING_URL = f"oracle+oracledb://{settings['db_user']}:{settings['db_pass']}@{settings['db_host']}:{settings['db_port']}/?service_name={settings['db_service']}"

engine = create_engine(
  ORACLE_STRING_URL,
  pool_pre_ping=True
  )
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)