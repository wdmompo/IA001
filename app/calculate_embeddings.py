import torch

from helpers.decorators import medir_tiempo_ms
from helpers.ia import model_encode
from logger import get_logger


logger = get_logger(__name__)


@medir_tiempo_ms
def calculate_embeddings(model, frases_de_referencia, opiniones, device) -> tuple[torch.Tensor, torch.Tensor]:

    # Codificar oraciones para obtener sus embeddings
    print(f"\nEncoding sentences (frases de referencia)...")
    embeddings_frases_de_referencia = model_encode(model, frases_de_referencia, device)
    logger.info(f"Sentences encoded.", extra={'model.device': model.device})
    # if DEBUG:
    #     print("Embeddings:")
    #     for i, embedding in enumerate(embeddings_frases_de_referencia):
    #         print(f"Sentence {i+1} embedding: {embedding[:5]}...")  # Mostrar solo los primeros 5 valores del embedding


    # Codificar oraciones para obtener sus embeddings
    print("\nEncoding sentences (opiniones)...")
    embeddings_opiniones = model_encode(model, opiniones, device)
    logger.info(f"Sentences encoded.", extra={'model.device': model.device})
    # if DEBUG:
    #     print("Embeddings:")
    #     for i, embedding in enumerate(embeddings_opiniones):
    #         print(f"Sentence {i+1} embedding: {embedding[:5]}...")  # Mostrar solo los primeros 5 valores del embedding

    return embeddings_frases_de_referencia, embeddings_opiniones
