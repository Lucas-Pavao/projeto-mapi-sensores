import os
import requests
import urllib3
import json
import time
from bs4 import BeautifulSoup
from src.utils.text_utils import remover_acentos
from dotenv import load_dotenv

load_dotenv()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class BaseApacCollector:
    _cache = {}
    _cache_ttl = 55  # Cache por 55 segundos (um pouco menos que o intervalo padrão)

    def __init__(self, endpoint_key):
        base_url = os.getenv("APAC_BASE_URL", "http://dados.apac.pe.gov.br:41120")
        endpoint = os.getenv(endpoint_key, endpoint_key.lower().replace("apac_", "").replace("_endpoint", ""))
        self.url = f"{base_url}/{endpoint}/"
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
        }

    def buscar_dados(self, filtro_cidade=None, filtro_estacao=None):
        try:
            agora = time.time()
            if self.url in self._cache:
                dados_cache, timestamp = self._cache[self.url]
                if agora - timestamp < self._cache_ttl:
                    todas_estacoes = dados_cache
                else:
                    todas_estacoes = self._fetch_new_data()
            else:
                todas_estacoes = self._fetch_new_data()

            if not todas_estacoes:
                return None

            resultado = todas_estacoes
            if filtro_cidade:
                resultado = self._filtrar_por_cidade(resultado, filtro_cidade)
            
            if filtro_estacao:
                resultado = self._filtrar_por_estacao(resultado, filtro_estacao)

            return resultado

        except Exception as e:
            print(f"Erro na coleta {self.__class__.__name__}: {e}")
            return None

    def _fetch_new_data(self):
        response = requests.get(self.url, headers=self.headers, verify=False, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        json_str = soup.body.text if soup.body else response.text

        dados_brutos = json.loads(json_str)
        todas_estacoes = self._parse_data(dados_brutos)
        
        self._cache[self.url] = (todas_estacoes, time.time())
        return todas_estacoes

    def _filtrar_por_cidade(self, estacoes, filtro_cidade):
        cidade_limpa = remover_acentos(filtro_cidade.upper())
        estacoes_filtradas = []
        for d in estacoes:
            muni_limpo = remover_acentos(d.get('municipio', '').upper())
            nome_estacao_limpo = remover_acentos(d.get('estacao_nome', '').upper())

            if cidade_limpa in muni_limpo or cidade_limpa in nome_estacao_limpo:
                estacoes_filtradas.append(d)
        return estacoes_filtradas

    def _filtrar_por_estacao(self, estacoes, filtro_estacao):
        estacao_limpa = remover_acentos(filtro_estacao.upper())
        for d in estacoes:
            nome_estacao_limpo = remover_acentos(d.get('estacao_nome', '').upper())
            codigo = str(d.get('codigo', ''))
            
            if estacao_limpa == nome_estacao_limpo or estacao_limpa == codigo:
                return [d]
        return []

    def _parse_data(self, dados_brutos):
        raise NotImplementedError("Subclasses devem implementar _parse_data")
