import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


class AuthManager:
    def __init__(self):
        self.url_auth = os.getenv("ANA_AUTH_URL", "https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas/OAUth/v1")
        self.identificador = os.getenv("ANA_IDENTIFICADOR")
        self.senha = os.getenv("ANA_SENHA")
        self.token = None
        self.expiracao = None

        # Configuração de Sessão com Retentativas (Retry)
        self.session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
            raise_on_status=False
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def obter_token(self):
        if self.token and datetime.now() < self.expiracao:
            return self.token

        headers = {
            "identificador": self.identificador,
            "senha": self.senha,
            "accept": "application/json"
        }

        try:
            # Adicionado timeout de 15 segundos
            response = self.session.get(self.url_auth, headers=headers, timeout=15)
            response.raise_for_status()

            dados = response.json()

            self.token = dados.get("items", {}).get("tokenautenticacao")

            if self.token:
                self.expiracao = datetime.now() + timedelta(minutes=59)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Token validado com sucesso!")

            return self.token

        except Exception as e:
            print(f"Erro ao obter token: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Resposta do servidor: {e.response.text}")
            return None