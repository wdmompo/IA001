from rich import print

from decorators import ProcessTime
from helpers.text_functions import limpiar_opiniones
from logger import get_logger


logger = get_logger(__name__)


@ProcessTime(__name__)
def opinions_cleaning(opiniones: list[str], expresiones_a_descartar: list[str]) -> list[str]:
    print("\n[green]Cleaning opinions...[/green]")
    logger.info(f"Cleaning opinions...")
    total_opinions_before_cleaning = len(opiniones)
    opiniones = limpiar_opiniones(opiniones, expresiones_a_descartar)
    total_opinions_after_cleaning = len(opiniones)
    opinions_cleaned_count = total_opinions_before_cleaning - total_opinions_after_cleaning
    logger.info(f"Cleaned opinions.", 
                extra={'opinions initial count': total_opinions_before_cleaning,
                       'opinions cleaned count': opinions_cleaned_count,
                       'opinions final count': total_opinions_after_cleaning})
    print(f"[green]Cleaned opinions: [red]{opinions_cleaned_count}[/red] de [red]{total_opinions_before_cleaning}[/red]. Final opinion count: [red]{total_opinions_after_cleaning}[/red].[/green]")
    return opiniones
