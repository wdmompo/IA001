from sentence_transformers import SentenceTransformer
import torch

from helpers.decorators import medir_tiempo_ms
from helpers.ia import model_similarity
from logger import get_logger


logger = get_logger(__name__)


@medir_tiempo_ms
def calculate_similarities(
    model: SentenceTransformer, 
    embeddings_frases_de_referencia: torch.Tensor, 
    embeddings_opiniones: torch.Tensor
    ) -> torch.Tensor:

    """
    Calcula las similitudes entre frases de referencia y opiniones.

    Args:
        model (SentenceTransformer): El modelo de embeddings.
        embeddings_frases_de_referencia (torch.Tensor): Embeddings de las frases de referencia.
        embeddings_opiniones (torch.Tensor): Embeddings de las opiniones.

    Returns:
        torch.Tensor: Tensor con las similitudes calculadas.
    """

    print("\nCalculating similarities...")
    # 4. Verificar qué métrica matemática utiliza el modelo por defecto
    print(f"Métrica de comparación interna del modelo: '{model.similarity_fn_name}'")
    logger.info(f"Métrica de comparación interna del modelo.", extra={'model.similarity_fn_name': model.similarity_fn_name})
    similarities = model_similarity(model, embeddings_frases_de_referencia, embeddings_opiniones)
    logger.info(f"Similarities calculated.", extra={'model.device': model.device})
    # if DEBUG:
    #     print("Similarities:")
    #     for i in range(len(similarities)):
    #         for j in range(len(similarities[i])):
    #             print(f"Similarity between sentence {i+1} and sentence {j+1}: {similarities[i][j]:.4f}")

    return similarities
