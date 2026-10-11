import json
import unicodedata
import re

rmr_municipios = [
    "RECIFE", "JABOATÃO DOS GUARARAPES", "OLINDA", "PAULISTA", "IGARASSU",
    "ABREU E LIMA", "CAMARAGIBE", "CABO DE SANTO AGOSTINHO", "IPOJUCA", "MORENO",
    "SÃO LOURENÇO DA MATA", "ARAÇOIABA", "ILHA DE ITAMARACÁ", "ITAPISSUMA",
    "JABOATAO DOS GUARARAPES", "SAO LOURENCO DA MATA", "ARACROIABA", "ITAMARACA"
]

rmr_stations_known = ["CASTELO BRANCO", "ENGENHO VELHO", "CURADO", "VILA NATAL", "ALTO DA BONDADE"]

def normalize(text):
    if not text: return ""
    return "".join(c for c in unicodedata.normalize('NFD', text.upper()) if unicodedata.category(c) != 'Mn')

rmr_norm = [normalize(m) for m in rmr_municipios]
rmr_stations_norm = [normalize(s) for s in rmr_stations_known]

def is_rmr(text):
    if not text: return False
    norm_text = normalize(text)
    
    # Busca por municípios (exato ou como parte de frase com limites de palavra)
    for m in rmr_norm:
        if re.search(r'\b' + re.escape(m) + r'\b', norm_text):
            return True
            
    # Busca por estações conhecidas
    for s in rmr_stations_norm:
        if re.search(r'\b' + re.escape(s) + r'\b', norm_text):
            return True
            
    # Caso especial para "PINA" (evitar Araripina)
    if re.search(r'\bPINA\b', norm_text):
        return True
        
    return False

def process_file(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    
    stations = {}
    for item in data:
        detalhes = json.loads(item.get("Dados_completos", "{}"))
        municipio = detalhes.get("cidade", "")
        estacao_nome = item.get("Estação", "")
        name_station = detalhes.get("nameStation", "")
        
        if is_rmr(municipio) or is_rmr(estacao_nome) or is_rmr(name_station):
            codigo = item.get("Codigo_gmmc")
            if codigo not in stations:
                stations[codigo] = {
                    "nome": estacao_nome,
                    "municipio": municipio or name_station or "RMR (identificado)",
                    "tipo": detalhes.get("tipo", "N/A")
                }
    return stations

print("--- CEMADEN RMR ---")
for cod, info in process_file("/home/lucas/Documents/exemplos/cemadem.txt").items():
    print(f"{cod}: {info['nome']} ({info['municipio']}) - {info['tipo']}")

print("\n--- METEOROLOGIA24H RMR ---")
for cod, info in process_file("/home/lucas/Documents/exemplos/meteorologia24h.txt").items():
    print(f"{cod}: {info['nome']} ({info['municipio']}) - {info['tipo']}")

