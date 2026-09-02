import logging

# from app import settings

def setup_logging():
    # logging.basicConfig(
    #     filename=settings.LOGGING_FILENAME,
    #     filemode=settings.LOGGING_FILEMODE,
    #     format=settings.LOGGING_FORMAT,
    #     encoding=settings.LOGGING_ENCODING,
    #     level=getattr(logging, str(settings.LOGGING_LEVEL).upper()),
    # )
    logging.basicConfig(
        filename="IA001.log",
        filemode="w",    # "w" para sobrescribir el archivo de log en cada ejecución, "a" para agregar al final del archivo
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
        level=logging.INFO,
    )

def get_logger(name=None):
    return logging.getLogger(name)
