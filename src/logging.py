import logging
from enum import Enum, StrEnum

LOG_FORMAT_DEBUG = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"


class LogLevels(StrEnum):
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    DEBUG = "DEBUG"


def configure_logging(log_level: LogLevels = LogLevels.ERROR):
    logging.basicConfig(level=log_level)
