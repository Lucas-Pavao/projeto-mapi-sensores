import unicodedata
import re

# Lista abrangente de municípios da Região Metropolitana do Recife (RMR)
# Inclui variações comuns e nomes normalizados
RMR_MUNICIPIOS = [
    "RECIFE", "JABOATAO DOS GUARARAPES", "OLINDA", "PAULISTA", "IGARASSU",
    "ABREU E LIMA", "CAMARAGIBE", "CABO DE SANTO AGOSTINHO", "IPOJUCA", "MORENO",
    "SAO LOURENCO DA MATA", "ARACOIABA", "ILHA DE ITAMARACA", "ITAPISSUMA",
    "GOIANA" # Goiana é frequentemente associada à RMR em contextos de monitoramento
]

# Estações ou termos conhecidos que indicam localização na RMR
RMR_TERMOS_ESPECIAIS = [
    "CASTELO BRANCO", "ENGENHO VELHO", "CURADO", "VILA NATAL", 
    "ALTO DA BONDADE", "PINA", "IMBIRIBEIRA", "NOVA DESCOBERTA", 
    "ALDEIA", "COMPESA", "SEDE"
]

def remover_acentos(txt):
    if not txt:
        return ""
    # Normaliza a string para separar os caracteres de seus acentos
    nfkd_form = unicodedata.normalize('NFKD', txt)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def normalizar_texto(txt):
    """Remove acentos, converte para maiúsculas e remove espaços extras."""
    if not txt:
        return ""
    return remover_acentos(txt).upper().strip()

def is_rmr(municipio, estacao_nome=""):
    """
    Verifica se um município ou nome de estação pertence à RMR.
    Utiliza regex para busca exata de palavras para evitar falsos positivos (ex: Araripina).
    """
    muni_norm = normalizar_texto(municipio)
    estacao_norm = normalizar_texto(estacao_nome)
    
    # 1. Busca por municípios da RMR
    for m in RMR_MUNICIPIOS:
        m_norm = normalizar_texto(m)
        pattern = r'\b' + re.escape(m_norm) + r'\b'
        if re.search(pattern, muni_norm) or re.search(pattern, estacao_norm):
            return True
            
    # 2. Busca por termos especiais
    for t in RMR_TERMOS_ESPECIAIS:
        t_norm = normalizar_texto(t)
        pattern = r'\b' + re.escape(t_norm) + r'\b'
        if re.search(pattern, estacao_norm) or re.search(pattern, muni_norm):
            return True
            
    return False
