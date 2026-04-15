import logging
import os.path
import sys
from logging.handlers import RotatingFileHandler

from app.core.JsonFormatter import JsonFormatter
from app.core.config import settings


def setup_logger(name: str = "pocket_attorney_rag") -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger

    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logger.setLevel(log_level)

    if settings.log_format == "json":
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

    # =============== console handler ============
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # =============== File handler ==============
    if settings.log_to_file:
        os.makedirs(os.path.dirname(settings.log_file), exist_ok=True)

        file_handler = RotatingFileHandler(
            filename=settings.log_file,
            maxBytes=10 * 1024 * 1024,
            backupCount=10,
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # ========= log after logger setup complete ==========
    logger.info("Logger initialized")

    return logger