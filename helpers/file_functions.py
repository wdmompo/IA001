from os import path

from decorators import ProcessTime
from logger import get_logger


logger = get_logger(__name__)


@ProcessTime(__name__)
def cargar_datos_desde_txt(nombre_archivo: str) -> list:
    try:
        print(f"Loading data from file: {path.join(path.join(path.dirname(path.dirname(__file__)), 'inputs'), nombre_archivo)}")
        with open(path.join(path.join(path.dirname(path.dirname(__file__)), "inputs"), nombre_archivo), 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        logger.error(f"File not found: {path.join(path.join(path.dirname(path.dirname(__file__)), 'inputs'), nombre_archivo)}")
        print(f"File not found: {path.join(path.join(path.dirname(path.dirname(__file__)), 'inputs'), nombre_archivo)}")
        return []
