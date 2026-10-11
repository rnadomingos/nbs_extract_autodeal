import os
import json
import logging
import urllib.request
import urllib.error
from typing import Dict, Any, Tuple, Optional

logger = logging.getLogger(__name__)

class AutonoxHttpClient:
    """
    Cliente HTTP resiliente para a API de Ingestão de OS do Autonox.
    """
    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None, timeout: int = 15):
        self.api_url = api_url or os.getenv("AUTONOX_API_URL", "https://autonox.com.br/api/ingest/os")
        self.api_key = api_key or os.getenv("AUTONOX_API_KEY", "")
        self.timeout = timeout

    def send_os(self, payload: Dict[str, Any], api_key: Optional[str] = None) -> Tuple[bool, int, Dict[str, Any], Optional[str]]:
        """
        Envia o payload de uma Ordem de Serviço para a API Autonox.
        
        Args:
            payload: Dicionário contendo os dados da OS.
            api_key: Chave da API da loja/empresa específica. Se não informada, tenta utilizar a chave default.
        
        Returns:
            Tuple[success: bool, status_code: int, response_json: dict, error_message: str | None]
        """
        active_api_key = api_key or self.api_key or os.getenv("AUTONOX_API_KEY", "")

        if not active_api_key:
            err_msg = "AUTONOX_API_KEY não informada para a empresa e não configurada no ambiente."
            logger.error(err_msg)
            return False, 401, {}, err_msg

        headers = {
            "Authorization": f"Bearer {active_api_key}",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "nbs-extract-autodeal/1.0"
        }

        data_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(self.api_url, data=data_bytes, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                status_code = resp.status
                body = resp.read().decode("utf-8")
                response_json = json.loads(body) if body else {}
                
                logger.info(f"Sucesso ao enviar OS {payload.get('numero_os')}: HTTP {status_code} - {response_json}")
                return True, status_code, response_json, None

        except urllib.error.HTTPError as e:
            status_code = e.code
            body = e.read().decode("utf-8") if e.fp else ""
            error_details = body
            try:
                error_json = json.loads(body)
                error_details = error_json.get("erro") or error_json.get("message") or body
            except Exception:
                pass
            
            err_msg = f"HTTPError {status_code}: {error_details}"
            logger.error(f"Erro ao enviar OS {payload.get('numero_os')}: {err_msg}")
            return False, status_code, {}, err_msg

        except urllib.error.URLError as e:
            err_msg = f"URLError (Falha de Conexão): {e.reason}"
            logger.error(f"Erro de rede ao enviar OS {payload.get('numero_os')}: {err_msg}")
            return False, 503, {}, err_msg

        except Exception as e:
            err_msg = f"Exceção inesperada: {str(e)}"
            logger.exception(f"Exceção ao enviar OS {payload.get('numero_os')}")
            return False, 500, {}, err_msg
