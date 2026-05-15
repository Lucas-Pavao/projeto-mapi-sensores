import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class AnaRestCollector:
    def __init__(self, auth_manager):
        self.base_url = os.getenv("ANA_BASE_URL", "https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas/HidroinfoanaSerieTelemetricaAdotada/v1")
        self.auth = auth_manager

    def buscar_dados(self, cod_estacao, data_busca, intervalo_busca="HORA_16", tipo_filtro="DATA_LEITURA"):
        token = self.auth.obter_token()

        if not token:
            print("Não foi possível obter um token válido.")
            return None

        url = self.base_url

        params = {
            "Código da Estação": cod_estacao,
            "Tipo Filtro Data": tipo_filtro,
            "Data de Busca (yyyy-MM-dd)": data_busca,
            "Range Intervalo de busca": intervalo_busca
        }

        headers = {
            "accept": "*/*",
            "authorization": f"Bearer {token}",  # Token dinâmico do AuthManager
            "referer": "https://www.ana.gov.br/hidrowebservice/swagger-ui/index.html",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
        }

        cookies = {
            "9e524b8a8cb4a6755c01a00f0ef52c2b": "bc719f6b4403d320ab156966a286d223"
        }

        try:
            # Adicionado timeout de 20 segundos para a coleta de dados
            response = requests.get(url, params=params, headers=headers, cookies=cookies, timeout=20)

            if response.status_code == 400:
                print(f"Erro 400 - Verifique se os nomes dos parâmetros estão corretos: {response.text}[cite: 485].")
                return None

            response.raise_for_status()
            return response.json()

        except Exception as e:
            print(f"Erro ao coletar dados REST: {e}[cite: 665].")
            return None