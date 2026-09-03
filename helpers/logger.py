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
