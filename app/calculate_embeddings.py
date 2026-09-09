from rich import print
from sentence_transformers import SentenceTransformer
import torch

from helpers.decorators import medir_tiempo_ms
from helpers.ia import model_encode
from logger import get_logger


logger = get_logger(__name__)


@medir_tiempo_ms
def calculate_embeddings(
    model: SentenceTransformer, 
    frases_de_referencia: list[str], 
    opiniones: list[str], 
    device: str
    ) -> tuple[torch.Tensor, torch.Tensor]:

    """
    Calcula los embeddings para las frases de referencia y las opiniones utilizando el modelo proporcionado.
    
    Args:
        model (SentenceTransformer): El modelo de embeddings.
        frases_de_referencia (list[str]): Lista de frases de referencia.
        opiniones (list[str]): Lista de opiniones.
        device (str): Dispositivo en el que realizar la codificación.

    Returns:
        tuple[torch.Tensor, torch.Tensor]: Tupla con los embeddings de las frases de referencia y las opiniones.
    """

    # Codificar oraciones para obtener sus embeddings
    print(f"\n[green]Encoding sentences (frases de referencia)...[/green]")
    embeddings_frases_de_referencia = model_encode(model, frases_de_referencia, device)
    logger.info(f"Sentences encoded.", extra={'model.device': model.device})
    logger.debug(f"Embeddings for frases de referencia calculated.", extra={'embeddings': embeddings_frases_de_referencia})
    #     print("Embeddings:")
    #     for i, embedding in enumerate(embeddings_frases_de_referencia):
    #         print(f"Sentence {i+1} embedding: {embedding[:5]}...")  # Mostrar solo los primeros 5 valores del embedding


    # Codificar oraciones para obtener sus embeddings
    print("\n[green]Encoding sentences (opiniones)...[/green]")
    embeddings_opiniones = model_encode(model, opiniones, device)
    logger.info(f"Sentences encoded.", extra={'model.device': model.device})
    logger.debug(f"Embeddings for opiniones calculated.", extra={'embeddings': embeddings_opiniones})
    #     print("Embeddings:")
    #     for i, embedding in enumerate(embeddings_opiniones):
    #         print(f"Sentence {i+1} embedding: {embedding[:5]}...")  # Mostrar solo los primeros 5 valores del embedding

    return embeddings_frases_de_referencia, embeddings_opiniones
