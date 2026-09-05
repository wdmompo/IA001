from os import path

from helpers.decorators import medir_tiempo_ms
from logger import get_logger


logger = get_logger(__name__)


@medir_tiempo_ms
def cargar_datos_desde_txt(nombre_archivo: str) -> list:
    try:
        print(f"Loading data from file: {path.join(path.join(path.dirname(path.dirname(__file__)), 'inputs'), nombre_archivo)}")
        with open(path.join(path.join(path.dirname(path.dirname(__file__)), "inputs"), nombre_archivo), 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        logger.error(f"File not found: {path.join(path.join(path.dirname(path.dirname(__file__)), 'inputs'), nombre_archivo)}")
        print(f"File not found: {path.join(path.join(path.dirname(path.dirname(__file__)), 'inputs'), nombre_archivo)}")
        return []
