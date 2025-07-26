from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from infra.load_settings import env_settings

database = 'POSTGRES'

load = env_settings(database)
settings = load.load_settings()

POSTGRES_STRING_URL = f"postgresql://{settings['db_user']}:{settings['db_pass']}@{settings['db_host']}:{settings['db_port']}/?{settings['db_service']}"

engine = create_engine(POSTGRES_STRING_URL)

Base = declarative_base

PostgresSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
