import requests
import json
import urllib3
import unicodedata
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def remover_acentos(txt):
    if not txt:
        return ""
    # Normaliza a string para separar os caracteres de seus acentos
    nfkd_form = unicodedata.normalize('NFKD', txt)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


class ApacCollectorMeteorologia24h:
    def __init__(self):
        self.url = "http://dados.apac.pe.gov.br:41120/meteorologia24h/"
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
            todas_estacoes = self._parse_json_apac(dados_brutos)

            if filtro_cidade:
                cidade_limpa = remover_acentos(filtro_cidade.upper())
                estacoes_filtradas = []
                for d in todas_estacoes:
                    # Verifica se o nome da cidade desejada está contido no município ou no nome da estação
                    muni_limpo = remover_acentos(d.get('municipio', '').upper())
                    nome_estacao_limpo = remover_acentos(d.get('estacao_nome', '').upper())

                    if cidade_limpa in muni_limpo or cidade_limpa in nome_estacao_limpo:
                        estacoes_filtradas.append(d)
                return estacoes_filtradas

            return todas_estacoes

        except Exception as e:
            print(f"Erro na coleta APAC: {e}")
            return None

    def _parse_json_apac(self, dados_brutos):
        resultados = []
        for item in dados_brutos:
            try:
                detalhes_str = item.get("Dados_completos", "{}")
                detalhes = json.loads(detalhes_str)

                nome_estacao = item.get("Estação", "Desconhecida")

                municipio = detalhes.get("cidade")
                if not municipio:
                    name_station = detalhes.get("nameStation", "")
                    if name_station:
                        municipio = name_station.split("(")[0].strip()  # Extrai JABOATAO de "JABOATAO (CENTRO)"

                if not municipio:
                    municipio = "Não informada"

                resultados.append({
                    'estacao_nome': nome_estacao,
                    'codigo': item.get("Codigo_gmmc"),
                    'data_hora': item.get("Data-hora") or detalhes.get("dataHora", "N/A"),
                    'latitude': detalhes.get("latitude"),
                    'longitude': detalhes.get("longitude"),
                    'municipio': municipio,
                    'temperatura_ar': detalhes.get("temperatura_ar") or detalhes.get("temperatura_inst"),
                    'umidade_relativa': detalhes.get("umidade_relativa") or detalhes.get("umidade_inst"),
                    'radiacao_solar': detalhes.get("radiacao_solar") or detalhes.get("radiacao_solar_global"),
                    'precipitacao_acumulada': float(
                        detalhes.get("precipitacao_acumulada") or detalhes.get("precipitacao_xx_00") or 0),
                    'umidade_solo': [
                        detalhes.get(f"umidade_solo_nivel{i}") or detalhes.get(f"umidade_solo_nivel{i}_media") for i in
                        range(1, 5)
                    ],
                    'tipo': detalhes.get("tipo", "Mista/N/A"),
                    'fonte': 'APAC/Meteorologia24h'
                })
            except (json.JSONDecodeError, ValueError) as e:
                continue
        return resultados