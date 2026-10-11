import json
from src.collectors.base_collector import BaseApacCollector

class ApacCollectorMeteorologia24h(BaseApacCollector):
    def __init__(self):
        super().__init__("APAC_METEOROLOGIA_ENDPOINT")

    def _parse_data(self, dados_brutos):
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
                        municipio = name_station.split("(")[0].strip()

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
                    'pressao_atmosferica': detalhes.get("pressao_atmosferica") or detalhes.get("pressao_inst"),
                    'velocidade_vento': detalhes.get("velocidade_vento") or detalhes.get("vento_velocidade"),
                    'direcao_vento': detalhes.get("direcao_vento") or detalhes.get("vento_direcao"),
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
            except (json.JSONDecodeError, ValueError):
                continue
        return resultados
