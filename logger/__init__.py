from .logger import LoggerFactory

LoggerFactory.configure()
get_logger = LoggerFactory.get_logger
