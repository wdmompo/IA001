from helpers.config import settings
from helpers.decorators import medir_tiempo_ms
from helpers.text_functions import limpiar_texto
from logger import get_logger


logger = get_logger(__name__)


@medir_tiempo_ms
def opinions_cleaning(opiniones: list[str]) -> list[str]:
    # Limpiar opiniones
    print("\nCleaning opinions...")
    logger.info(f"Cleaning opinions...")
    opiniones = [opinion for opinion in opiniones if opinion.strip()]
    print(f"Opinions after removing empty lines: {len(opiniones)}")
    opiniones = [limpiar_texto(opinion) for opinion in opiniones if limpiar_texto(opinion)]
    logger.info(f"Cleaned opinions.", extra={'opinions count': len(opiniones)})
    print(f"Cleaned opinions: {len(opiniones)}")
    return opiniones
