import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
from helpers.config import settings
from .formatters import JsonFormatter, get_text_formatter

class LoggerFactory:
    _initialized = False

    @classmethod
    def configure(cls):
        if cls._initialized:
            return

        root_logger = logging.getLogger()
        root_logger.handlers.clear()
        root_logger.setLevel(getattr(logging, settings.LOGGING_LEVEL.upper(), logging.INFO))

        formatter = JsonFormatter() if settings.LOGGING_FORMAT_TYPE.lower() == 'json' else get_text_formatter()

        log_output = [d.strip().lower() for d in settings.LOGGING_MODE.split(",")]

        if "console" in log_output:
            sh = logging.StreamHandler()
            sh.setFormatter(formatter)
            root_logger.addHandler(sh)

        if "file" in log_output:
            path = Path(settings.LOGGING_FILENAME)
            path.parent.mkdir(parents=True, exist_ok=True)
            fh = RotatingFileHandler(
                filename=path, 
                mode=settings.LOGGING_FILEMODE, 
                maxBytes=settings.LOGGING_MAX_BYTES, 
                backupCount=settings.LOGGING_BACKUP_COUNT, 
                encoding=settings.LOGGING_ENCODING)
            fh.setFormatter(formatter)
            root_logger.addHandler(fh)

        cls._initialized = True

    @staticmethod
    def get_logger(name=None):
        return logging.getLogger(name)
