import pandas as pd
import re

from helpers.config import settings


def limpiar_texto(texto) -> str:
    if pd.isna(texto):
        return ""
    texto = str(texto)
    texto = texto.strip()
    texto = texto.lower()
    if settings.TEXT_CLEAN_REMOVE_ACCENTS:
        texto = re.sub('[áÁ]', 'a', texto)
        texto = re.sub('[éÉ]', 'e', texto)
        texto = re.sub('[íÍ]', 'i', texto)
        texto = re.sub('[óÓ]', 'o', texto)
        texto = re.sub('[úÚ]', 'u', texto)
    if settings.TEXT_CLEAN_REMOVE_ENIE:
        texto = re.sub('[ñÑ]', 'n', texto)
    if settings.TEXT_CLEAN_REMOVE_SPECIAL_CHARACTERS:
        texto = re.sub(r'<.*?>', ' ', texto)
        texto = re.sub(r'\s+', ' ', texto)
        texto = re.sub('[^a-zA-Z]', ' ', texto)
    return texto


def limpiar_opiniones(opiniones: list[str], expresiones_a_descartar: list[str]) -> list[str]:
    return [limpiar_texto(opinion) 
            for opinion in opiniones 
                if limpiar_texto(opinion) 
                and not any(opinion.lower() in expresion.lower() for expresion in expresiones_a_descartar)
                and len(opinion) >= settings.TEXT_CLEAN_MINIMUM_LENGTH
                and len(opinion.split()) >= settings.TEXT_CLEAN_MINIMUM_WORD_COUNT
    ]
