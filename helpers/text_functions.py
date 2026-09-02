import pandas as pd
import re


# @medir_tiempo_ms
def limpiar_texto(texto) -> str:
    if pd.isna(texto):
        return ""
    texto = str(texto)
    texto = texto.lower()
    texto = re.sub(r'<.*?>', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto)
    texto = texto.strip()
    texto = re.sub('[áÁ]', 'a', texto)
    texto = re.sub('[éÉ]', 'e', texto)
    texto = re.sub('[íÍ]', 'i', texto)
    texto = re.sub('[óÓ]', 'o', texto)
    texto = re.sub('[úÚ]', 'u', texto)
    texto = re.sub('[ñÑ]', 'n', texto)
    texto = re.sub('[^a-zA-Z]', ' ', texto)
    return texto
