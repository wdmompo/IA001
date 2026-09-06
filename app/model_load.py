from sentence_transformers import SentenceTransformer

from helpers.decorators import medir_tiempo_ms
from helpers.ia import get_model_device
from helpers.ia import model_load as ml
from logger import get_logger


logger = get_logger(__name__)


@medir_tiempo_ms
def model_load(
    model_name: str, 
    device: str
    ) -> SentenceTransformer:

    """
    Carga un modelo preentrenado.

    Args:
        model (str): Nombre del modelo a cargar.
        device (str): Dispositivo en el que cargar el modelo.

    Returns:
        El modelo cargado.
    """

    # Cargar un modelo preentrenado
    print(f"\nLoading model {model_name}...")
    logger.info(f"Loading model...", extra={'model': model_name})
    # Detectar automáticamente el mejor dispositivo disponible
    device = get_model_device()
    model_st = SentenceTransformer(model_name, device=device)
    try:
        model_st = ml(model_name, device)
    except Exception as e:
        logger.info(f"Error loading model.", extra={'model': model_name, 'error': e})
        print(f"Error loading model {e}.")
    else:
        logger.info(f"Model loaded successfully.", extra={'model': model_name, 'device': model_st.device})
        print(f"Model {model_name} loaded successfully in {model_st.device}.")

    return model_st
