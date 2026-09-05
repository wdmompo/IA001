from sentence_transformers import SentenceTransformer

from helpers.decorators import medir_tiempo_ms
from helpers.ia import get_model_device
from logger import get_logger


logger = get_logger(__name__)


@medir_tiempo_ms
def model_load(model, device) -> SentenceTransformer:
    """
    Carga un modelo preentrenado.

    Args:
        model (str): Nombre del modelo a cargar.
        device: Dispositivo en el que cargar el modelo.

    Returns:
        El modelo cargado.
    """
    # Cargar un modelo preentrenado
    print(f"\nLoading model {model}...")
    logger.info(f"Loading model...", extra={'model': model})
    # Detectar automáticamente el mejor dispositivo disponible
    device = get_model_device()
    try:
        model = model_load(model, device)
    except Exception as e:
        logger.info(f"Error loading model.", extra={'model': model, 'error': e})
        print(f"Error loading model {e}.")
    else:
        logger.info(f"Model loaded successfully.", extra={'model.device': model.device})
        print(f"Model loaded successfully in {model.device}.")

    return model
