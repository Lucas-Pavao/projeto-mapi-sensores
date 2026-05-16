import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
class AnaRestCollector:
    def __init__(self, auth_manager):
        self.base_url = os.getenv("ANA_BASE_URL", "https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas/HidroinfoanaSerieTelemetricaAdotada/v1")
        self.inventory_url = os.getenv("ANA_INVENTARIO_URL", "https://www.ana.gov.br/hidrowebservice/EstacoesTelemetricas/HidroInventarioEstacoes/v1")
        self.auth = auth_manager
        self._metadata_cache = {}

    def buscar_inventario(self, cod_estacao):
        """Retorna os dados cadastrais da estação (Latitude, Longitude, etc.)"""
        if cod_estacao in self._metadata_cache:
            return self._metadata_cache[cod_estacao]

        token = self.auth.obter_token()
        if not token:
            return None

        params = {"Código da Estação": cod_estacao}
        headers = {
            "accept": "*/*",
            "authorization": f"Bearer {token}",
            "referer": "https://www.ana.gov.br/hidrowebservice/swagger-ui/index.html",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
        }
        cookies = {
            "9e524b8a8cb4a6755c01a00f0ef52c2b": "bc719f6b4403d320ab156966a286d223"
        }

        try:
            response = requests.get(self.inventory_url, params=params, headers=headers, cookies=cookies, timeout=15)
            response.raise_for_status()
            data = response.json()

            if data and "items" in data and len(data["items"]) > 0:
                metadata = data["items"][0]
                self._metadata_cache[cod_estacao] = metadata
                return metadata
        except Exception as e:
            print(f"Erro ao buscar inventário ANA para {cod_estacao}: {e}")

        return None

    def buscar_dados(self, cod_estacao, data_busca, intervalo_busca="HORA_16", tipo_filtro="DATA_LEITURA"):
        token = self.auth.obter_token()

        if not token:
            print("Não foi possível obter um token válido.")
            return None

        # 1. Buscar dados de medição
        params = {
            "Código da Estação": cod_estacao,
            "Tipo Filtro Data": tipo_filtro,
            "Data de Busca (yyyy-MM-dd)": data_busca,
            "Range Intervalo de busca": intervalo_busca
        }

        headers = {
            "accept": "*/*",
            "authorization": f"Bearer {token}",
            "referer": "https://www.ana.gov.br/hidrowebservice/swagger-ui/index.html",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
        }

        cookies = {
            "9e524b8a8cb4a6755c01a00f0ef52c2b": "bc719f6b4403d320ab156966a286d223"
        }

        try:
            response = requests.get(self.base_url, params=params, headers=headers, cookies=cookies, timeout=20)

            if response.status_code == 400:
                print(f"Erro 400 - Verifique se os nomes dos parâmetros estão corretos: {response.text}")
                return None

            response.raise_for_status()
            dados_medicao = response.json()

            # 2. Buscar metadados (inventário) para cruzar
            metadados = self.buscar_inventario(cod_estacao)

            # 3. Cruzar dados (Join)
            if metadados and "items" in dados_medicao:
                for item in dados_medicao["items"]:
                    item["Latitude"] = metadados.get("Latitude")
                    item["Longitude"] = metadados.get("Longitude")
                    item["Estacao_Nome"] = metadados.get("Estacao_Nome")
                    item["Bacia_Nome"] = metadados.get("Bacia_Nome")
                    item["Municipio_Nome"] = metadados.get("Municipio_Nome")

            return dados_medicao

        except Exception as e:
            print(f"Erro ao coletar dados REST da ANA: {e}")
            return None