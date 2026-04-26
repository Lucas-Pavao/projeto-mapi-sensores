import json
from src.collectors.base_collector import BaseApacCollector

class ApacCemadenCollector(BaseApacCollector):
    def __init__(self):
        super().__init__("cemaden")

    def _parse_data(self, dados_brutos):
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
                    'codigo': item.get("Codigo_gmmc"),
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
