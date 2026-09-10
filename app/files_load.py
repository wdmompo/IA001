from rich import print

from helpers.config import settings
from helpers.decorators import medir_tiempo_ms
from helpers.file_functions import cargar_datos_desde_txt
from logger import get_logger


logger = get_logger(__name__)


@medir_tiempo_ms
def files_load() -> tuple[list[str], list[str], list[str]]:
    # Carga de expresiones a descartar
    print("\n[green]Loading expressions to discard...[/green]")
    logger.info(f"Loading expressions to discard...")
    expresiones_a_descartar = cargar_datos_desde_txt(settings.INPUTS_EXPRESIONES_A_DESCARTAR)
    expresiones_a_descartar.append("")
    logger.info(f"Loaded {len(expresiones_a_descartar)} expressions to discard.")
    print(f"[green]Loaded [red]{len(expresiones_a_descartar)}[/red] expressions to discard.[/green]")
    logger.debug(f"Expressions to discard: {expresiones_a_descartar}")
    # if DEBUG:
    #     print(f"Expressions to discard:")
    #     for i, expresion in enumerate(expresiones_a_descartar):
    #         print(f"Expression {i+1}: {expresion}")


    # Carga de frases de referencia
    print("\n[green]Loading reference sentences...[/green]")
    logger.info(f"Loading reference sentences...")
    frases_de_referencia = cargar_datos_desde_txt(settings.INPUTS_FRASES_DE_REFERENCIA)
    logger.info(f"Loaded {len(frases_de_referencia)} reference sentences.")
    print(f"[green]Loaded [red]{len(frases_de_referencia)}[/red] reference sentences.[/green]")
    logger.debug(f"Reference sentences: {frases_de_referencia}")
    # if DEBUG:
    #     print(f"Reference sentences:")
    #     for i, sentence in enumerate(frases_de_referencia):
    #         print(f"Sentence {i+1}: {sentence}")


    # Carga de opiniones
    print("\n[green]Loading opinions...[/green]")
    logger.info(f"Loading opinions...")
    opiniones = cargar_datos_desde_txt(settings.INPUTS_OPINIONES)
    logger.info(f"Loaded {len(opiniones)} opinions.")
    print(f"[green]Loaded [red]{len(opiniones)}[/red] opinions.[/green]")
    logger.debug(f"Opinions: {opiniones}")
    # if DEBUG:
    #     print(f"Opinions:")
    #     for i, opinion in enumerate(opiniones):
    #         print(f"Opinion {i+1}: {opinion}")


    return expresiones_a_descartar, frases_de_referencia, opiniones
