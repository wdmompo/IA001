from functools import wraps
import time

from logger import get_logger


logger = get_logger(__name__)


class ProcessTime:
    def __init__(self, name: str):
        self.name = name

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end_time = time.perf_counter()
        self.duration_ms = (self.end_time - self.start_time) * 1000
        logger.info(f"Process Time: ({self.name}) {self.duration_ms:.2f} ms")

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return wrapper
    