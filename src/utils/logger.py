from logging import getLogger, Logger, Formatter, StreamHandler
from logging.handlers import TimedRotatingFileHandler
from os import makedirs

from config import config


def init_logger() -> Logger:
    makedirs(config.LOGS_PATH, exist_ok=True)
    logger = create_logger(
        config.SERVICE_NAME,
        config.LOGS_PATH,
    )
    logger.info(f"Service {config.SERVICE_NAME!r} successfully started.")

    return logger

def create_logger(
        logger_name: str,
        filepath: str,
        logger_level: str = "DEBUG",
) -> Logger:
    formatter = Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%d.%m.%Y %H:%M:%S"
    )
    logger = getLogger(logger_name)
    logger.setLevel(logger_level)
    logger.handlers = []

    console_handler = StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = TimedRotatingFileHandler(
        f"{filepath}/{logger_name}.log",
        when="midnight"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


logger = init_logger()
