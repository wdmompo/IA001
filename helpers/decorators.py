from functools import wraps
import time

from logger import get_logger


logger = get_logger(__name__)


def medir_tiempo_ms(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        duracion_ms = (time.perf_counter() - inicio) * 1000
        logger.info(f"Proccess Time: ({func.__name__}) {duracion_ms:.2f} ms")
        return resultado
    return wrapper
