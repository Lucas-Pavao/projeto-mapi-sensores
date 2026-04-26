import unicodedata

def remover_acentos(txt):
    if not txt:
        return ""
    # Normaliza a string para separar os caracteres de seus acentos
    nfkd_form = unicodedata.normalize('NFKD', txt)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
