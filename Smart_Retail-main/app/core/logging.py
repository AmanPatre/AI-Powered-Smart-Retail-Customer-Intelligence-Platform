"""Application-wide structured logging configuration."""

import sys
import logging
from app.core.config import settings


def setup_logging() -> logging.Logger:
    """Configure system logger with console output and formatting."""
    logger = logging.getLogger("smart_retail")
    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


logger = setup_logging()
