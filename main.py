from rich import print

from app.calculate_embeddings import calculate_embeddings
from app.calculate_similarities import calculate_similarities
from app.data_cleaning import opinions_cleaning
from app.files_load import files_load
from app.model_load import model_load
from helpers.config import settings
from helpers.decorators import medir_tiempo_ms
from helpers.ia import get_model_device
from logger import get_logger


logger = get_logger(__name__)


@medir_tiempo_ms
def main():
    print(f"[orange_red1]*****[/orange_red1] [bold blue]Starting the script with model:[/bold blue] [red]{settings.MODEL_NAME}[/red]")
    logger.info(f"Starting the script with model", extra={'model': settings.MODEL_NAME})

    device = get_model_device()

    # Proceso general
    expresiones_a_descartar, frases_de_referencia, opiniones = files_load()
    opiniones = opinions_cleaning(opiniones, expresiones_a_descartar)
    model = model_load(settings.MODEL_NAME, device)
    embeddings_frases_de_referencia, embeddings_opiniones = calculate_embeddings(model, frases_de_referencia, opiniones, device)
    similarities = calculate_similarities(model, embeddings_frases_de_referencia, embeddings_opiniones)


    logger.info("Script completed.")
    print("[orange_red1]*****[/orange_red1] [bold blue]Script completed.[/bold blue]")


if __name__ == "__main__":
    main()
