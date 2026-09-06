from sentence_transformers import SentenceTransformer
import torch
import truststore

from helpers.decorators import medir_tiempo_ms
from logger import get_logger


logger = get_logger(__name__)


@medir_tiempo_ms
def get_model_device() -> str:

    """
    Detecta automáticamente el mejor dispositivo disponible para ejecutar el modelo de embeddings.

    Returns:
        str: El nombre del dispositivo detectado ("cuda", "mps", "xpu" o "cpu").
    """

    # Detectar automáticamente el mejor dispositivo disponible
    # device = "cuda" if torch.cuda.is_available() else "cpu"
    # 1. Verificar si hay GPU de NVIDIA (CUDA)
    if torch.cuda.is_available():
        device = "cuda"
    # 2. Verificar si hay GPU de Apple Silicon (M1/M2/M3)
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device = "mps"
    # 3. Verificar si hay GPU de Intel (XPU) - Común en arquitecturas modernas
    elif hasattr(torch, "xpu") and torch.xpu.is_available():
        device = "xpu"
    # 4. Si ninguna opción está disponible, usar el procesador principal
    else:
        device = "cpu"
    return device


@medir_tiempo_ms
def model_load(
    model_name_or_path: str, 
    device: str
    ) -> SentenceTransformer:

    """
    Carga un modelo de transformers para la generación de embeddings.

    Args:
        model_name_or_path (str): El nombre o la ruta del modelo.
        device (str): El dispositivo en el que cargar el modelo.

    Returns:
        SentenceTransformer: El modelo cargado.
    """

    truststore.inject_into_ssl()
    model = SentenceTransformer(
        model_name_or_path=model_name_or_path,
        device=device,  # "cuda", "cpu", "mps", "npu"
    )
    return model


@medir_tiempo_ms
def model_encode(
    model: SentenceTransformer, 
    sentences: list, 
    device: str
    ) -> torch.Tensor:

    """
    Codifica una lista de oraciones utilizando el modelo de embeddings proporcionado.
    
    Args:
        model (SentenceTransformer): El modelo de embeddings.
        sentences (list): Lista de oraciones a codificar.
        device (str): El dispositivo en el que realizar la codificación.

    Returns:
        torch.Tensor: Los embeddings codificados.
    """

    return model.encode(
        inputs=sentences,
        device=device,
        show_progress_bar=True,
        convert_to_tensor=True,
        normalize_embeddings=True
    )


@medir_tiempo_ms
def model_similarity(
    model: SentenceTransformer, 
    embeddings_a: torch.Tensor, 
    embeddings_b: torch.Tensor
    ) -> torch.Tensor:

    """
    Calcula la similitud entre dos conjuntos de embeddings utilizando el modelo proporcionado.

    Args:
        model (SentenceTransformer): El modelo de embeddings.
        embeddings_a (torch.Tensor): Primer conjunto de embeddings.
        embeddings_b (torch.Tensor): Segundo conjunto de embeddings.
    Returns:
        torch.Tensor: Matriz de similitud entre los dos conjuntos de embeddings.
    """
    
    similarities = model.similarity(embeddings_a, embeddings_b)
    return similarities
