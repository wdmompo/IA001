import json
import logging
from datetime import datetime
from helpers.config import settings

# TEXT_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(module)s:%(lineno)d | %(message)s"
TEXT_FORMAT = settings.LOGGING_FORMAT

STANDARD_ATTRS = set(logging.makeLogRecord({}).__dict__.keys())

class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            # "service": settings.SERVICE_NAME,
            # "environment": settings.ENVIRONMENT,
            # "version": settings.VERSION,
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
        }

        extra_data = {k:v for k,v in record.__dict__.items() if k not in STANDARD_ATTRS}
        if extra_data:
            payload["extra"] = extra_data

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, ensure_ascii=False)

def get_text_formatter():
    class TextFormatter(logging.Formatter):
        def format(self, record):
            extra_data = {
                key: value
                for key, value in record.__dict__.items()
                if key not in STANDARD_ATTRS and key not in {"message", "asctime"}
            }

            message = super().format(record)

            if extra_data:
                message += f" | extra={json.dumps(extra_data, ensure_ascii=False, default=str)}"

            return message

    return TextFormatter(TEXT_FORMAT)
