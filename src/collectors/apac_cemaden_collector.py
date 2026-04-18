import requests
import json
import urllib3
import unicodedata
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def remover_acentos(txt):
    if not txt:
        return ""
    nfkd_form = unicodedata.normalize('NFKD', txt)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


class ApacCemadenCollector:
    def __init__(self):
        self.url = "http://dados.apac.pe.gov.br:41120/cemaden/"

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'PHPSESSID=9f1102526426402b96eee6d3903e0bff; sc_actual_lang_Sirh=pt_br',
            'Referer': 'http://dados.apac.pe.gov.br:41120/dadosApac/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
        }

    def buscar_dados(self, filtro_cidade=None):
        try:
            response = requests.get(self.url, headers=self.headers, verify=False, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            json_str = soup.body.text if soup.body else response.text

            dados_brutos = json.loads(json_str)
            todas_estacoes = self._parse_json_cemaden(dados_brutos)

            if filtro_cidade:
                cidade_limpa = remover_acentos(filtro_cidade.upper())
                estacoes_filtradas = []
                for d in todas_estacoes:
                    muni_limpo = remover_acentos(d.get('municipio', '').upper())
                    nome_estacao_limpo = remover_acentos(d.get('estacao_nome', '').upper())

                    if cidade_limpa in muni_limpo or cidade_limpa in nome_estacao_limpo:
                        estacoes_filtradas.append(d)
                return estacoes_filtradas

            return todas_estacoes

        except Exception as e:
            print(f"Erro na coleta APAC (Cemaden): {e}")
            return None

    def _parse_json_cemaden(self, dados_brutos):
        resultados = []
        for item in dados_brutos:
            try:
                detalhes_str = item.get("Dados_completos", "{}")
                detalhes = json.loads(detalhes_str)

                municipio = detalhes.get("cidade", "Não informada").strip()

                chuva_str = detalhes.get("chuva", 0)
                try:
                    chuva_val = float(chuva_str) if chuva_str is not None else 0.0
                except ValueError:
                    chuva_val = 0.0

                resultados.append({
                    'estacao_nome': item.get("Estação", "Desconhecida"),
                    'codigo': item.get("Codigo_gmmc"),  # ESTA É A CHAVE PRIMÁRIA PARA O CRUZAMENTO FUTURO
                    'data_hora': item.get("Data-hora"),
                    'latitude': detalhes.get("latitude"),
                    'longitude': detalhes.get("longitude"),
                    'municipio': municipio,
                    'chuva_acumulada': chuva_val,
                    'tipo': detalhes.get("tipo", "Pluviométrica"),
                    'fonte': 'APAC/Cemaden'
                })
            except (json.JSONDecodeError, ValueError):
                continue
        return resultados