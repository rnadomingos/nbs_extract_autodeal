import os
import logging
from sqlalchemy import text
from sqlalchemy.engine import Engine
from include.infra.postgres_database import engine as default_engine

logger = logging.getLogger(__name__)

INITIAL_EMPRESA_SEEDS = [
    {
        "codigo_empresa": 2,
        "sigla": "GPBB",
        "marca": "BMW",
        "api_key_env_var": "AUTONOX_API_KEY_EMP_2",
        "default_api_key": "nox_sk_704L7xUmOG9zXxWr-1qhx8SfkFgO4OJY",
        "is_active": True,
    },
    # {
    #     "codigo_empresa": 3,
    #     "sigla": "GPBL",
    #     "marca": "BMW",
    #     "api_key_env_var": "AUTONOX_API_KEY_EMP_3",
    #     "default_api_key": "key_empresa_3_placeholder",
    #     "is_active": True,
    # },
    # {
    #     "codigo_empresa": 4,
    #     "sigla": "GPBC",
    #     "marca": "BMW",
    #     "api_key_env_var": "AUTONOX_API_KEY_EMP_4",
    #     "default_api_key": "key_empresa_4_placeholder",
    #     "is_active": True,
    # },
]


def seed_empresa_config(engine: Engine = default_engine) -> int:
    """
    Popula a tabela autonox_empresa_config com as empresas/lojas iniciais se ainda não existirem.

    Returns:
        int: Quantidade de registros inseridos/atualizados na seed.
    """
    query = text(
        """
        INSERT INTO autonox_empresa_config (codigo_empresa, sigla, marca, api_key, is_active, created_at, updated_at)
        VALUES (:codigo_empresa, :sigla, :marca, :api_key, :is_active, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        ON CONFLICT (codigo_empresa) DO UPDATE
        SET sigla = EXCLUDED.sigla,
            marca = EXCLUDED.marca,
            is_active = EXCLUDED.is_active,
            updated_at = CURRENT_TIMESTAMP
    """
    )

    global_api_key = os.getenv("AUTONOX_API_KEY", "")
    inserted_count = 0

    with engine.begin() as conn:
        for item in INITIAL_EMPRESA_SEEDS:
            env_key = os.getenv(item["api_key_env_var"], "")
            api_key = env_key or global_api_key or item["default_api_key"]

            result = conn.execute(
                query,
                {
                    "codigo_empresa": item["codigo_empresa"],
                    "sigla": item["sigla"],
                    "marca": item["marca"],
                    "api_key": api_key,
                    "is_active": item["is_active"],
                },
            )
            inserted_count += result.rowcount

    logger.info(
        f"Seed de autonox_empresa_config executada com sucesso. Registros afetados: {inserted_count}"
    )
    return inserted_count


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    seed_empresa_config()
