import logging

from core.config import config  # type: ignore


def get_logger(name: str):
    """Get logger"""
    # Create individual module-grained named loggers
    return logging.getLogger(name)


def setup_logger(logger: logging.Logger):
    """Logger setup"""
    # Create logging handlers
    c_handler = logging.StreamHandler()

    # Create formatters and add it to handlers
    c_format = logging.Formatter("%(name)s - %(levelname)s: %(message)s")
    c_handler.setFormatter(c_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.setLevel(config.loglevel)

    return logger
