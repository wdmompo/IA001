import logging

from helpers.config import settings


def setup_logging():
    logging.basicConfig(
        filename=settings.LOGGING_FILENAME,
        filemode=settings.LOGGING_FILEMODE,
        format=settings.LOGGING_FORMAT,
        encoding=settings.LOGGING_ENCODING,
        level=getattr(logging, str(settings.LOGGING_LEVEL).upper()),
    )


def get_logger(name=None):
    return logging.getLogger(name)




    # logger = logging.getLogger(__name__)
    # # logging.StreamHandler()       # Consola
    # # logging.FileHandler("app.log") # Archivo
    # # logging.handlers.RotatingFileHandler(...) # Archivo con rotación
    # # logging.handlers.SMTPHandler(...) # Correo electrónico
    # console = logging.StreamHandler()
    # console.setLevel(getattr(logging, str(settings.LOGGING_LEVEL).upper()))
    # console.setFormatter(logging.Formatter(settings.LOGGING_FORMAT))
    # file = logging.FileHandler(
    #         filename=settings.LOGGING_FILENAME,
    #         mode=settings.LOGGING_FILEMODE,
    #         encoding=settings.LOGGING_ENCODING,
    #     )
    # file.setLevel(getattr(logging, str(settings.LOGGING_LEVEL).upper()))
    # file.setFormatter(logging.Formatter(settings.LOGGING_FORMAT))
    # destinos = [d.strip().lower() for d in settings.LOGGING_MODE.split(",")]
    # if "console" in destinos:
    #     logger.addHandler(console)
    # if "file" in destinos:
    #     logger.addHandler(file)
    # if "database" in destinos:
    #     pass
    #     # from helpers.database_logger import DatabaseHandler
    #     # db_handler = DatabaseHandler(
    #     #     db_url=settings.LOGGING_DATABASE_URL,
    #     #     table_name=settings.LOGGING_DATABASE_TABLE
    #     # )
    #     # db_handler.setLevel(getattr(logging, str(settings.LOGGING_LEVEL).upper()))
    #     # logger.addHandler(db_handler)
