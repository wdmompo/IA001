from sentence_transformers import SentenceTransformer
import torch
import truststore

from helpers.decorators import medir_tiempo_ms
from logger import get_logger


logger = get_logger(__name__)


@medir_tiempo_ms
def get_model_device() -> str:
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
def model_load(model_name_or_path: str, device: str) -> SentenceTransformer:
    truststore.inject_into_ssl()
    model = SentenceTransformer(
        model_name_or_path=model_name_or_path,
        device=device,  # "cuda", "cpu", "mps", "npu"
    )
    return model


@medir_tiempo_ms
def model_encode(model: SentenceTransformer, sentences: list, device: str) -> torch.Tensor:
    return model.encode(
        inputs=sentences,
        device=device,
        show_progress_bar=True,
        convert_to_tensor=True,
        normalize_embeddings=True,
    )


@medir_tiempo_ms
def model_similarity(model: SentenceTransformer, embeddings_a: torch.Tensor, embeddings_b: torch.Tensor) -> torch.Tensor:
    similarities = model.similarity(embeddings_a, embeddings_b)
    return similarities
