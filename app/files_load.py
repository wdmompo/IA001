from helpers.config import settings
from helpers.decorators import medir_tiempo_ms
from helpers.file_functions import cargar_datos_desde_txt
from logger import get_logger

logger = get_logger(__name__)


@medir_tiempo_ms
def files_load() -> tuple[list[str], list[str], list[str]]:
    # Carga de expresiones a descartar
    print("\nLoading expressions to discard...")
    logger.info(f"Loading expressions to discard...")
    expresiones_a_descartar = cargar_datos_desde_txt(settings.INPUTS_EXPRESIONES_A_DESCARTAR)
    expresiones_a_descartar.append("")
    logger.info(f"Loaded {len(expresiones_a_descartar)} expressions to discard.")
    print(f"Loaded {len(expresiones_a_descartar)} expressions to discard.")
    logger.debug(f"Expressions to discard: {expresiones_a_descartar}")
    # if DEBUG:
    #     print(f"Expressions to discard:")
    #     for i, expresion in enumerate(expresiones_a_descartar):
    #         print(f"Expression {i+1}: {expresion}")


    # Carga de frases de referencia
    print("\nLoading reference sentences...")
    logger.info(f"Loading reference sentences...")
    frases_de_referencia = cargar_datos_desde_txt(settings.INPUTS_FRASES_DE_REFERENCIA)
    logger.info(f"Loaded {len(frases_de_referencia)} reference sentences.")
    print(f"Loaded {len(frases_de_referencia)} reference sentences.")
    logger.debug(f"Reference sentences: {frases_de_referencia}")
    # if DEBUG:
    #     print(f"Reference sentences:")
    #     for i, sentence in enumerate(frases_de_referencia):
    #         print(f"Sentence {i+1}: {sentence}")


    # Carga de opiniones
    print("\nLoading opinions...")
    logger.info(f"Loading opinions...")
    opiniones = cargar_datos_desde_txt(settings.INPUTS_OPINIONES)
    logger.info(f"Loaded {len(opiniones)} opinions.")
    print(f"Loaded {len(opiniones)} opinions.")
    logger.debug(f"Opinions: {opiniones}")
    # if DEBUG:
    #     print(f"Opinions:")
    #     for i, opinion in enumerate(opiniones):
    #         print(f"Opinion {i+1}: {opinion}")


    return expresiones_a_descartar, frases_de_referencia, opiniones
