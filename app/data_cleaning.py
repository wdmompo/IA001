from rich import print

from helpers.decorators import medir_tiempo_ms
from helpers.text_functions import limpiar_opiniones
from logger import get_logger


logger = get_logger(__name__)


@medir_tiempo_ms
def opinions_cleaning(opiniones: list[str], expresiones_a_descartar: list[str]) -> list[str]:
    print("\n[green]Cleaning opinions...[/green]")
    logger.info(f"Cleaning opinions...")
    opiniones = limpiar_opiniones(opiniones, expresiones_a_descartar)
    logger.info(f"Cleaned opinions.", extra={'opinions count': len(opiniones)})
    print(f"[green]Cleaned opinions: [/green][red]{len(opiniones)}[/red][green].[/green]")
    return opiniones
