"""
Logging Configuration
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from app.core.settings import settings


def configure_logging() -> None:
    """
    Configure global logger settings.
    """
    log_level = settings.LOG_LEVEL.upper()
    log_file = settings.LOG_FILE

    # Ensure log directory exists
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

    # Formatters
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)

    # Handlers
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    handlers: list[logging.Handler] = [console_handler]

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format=log_format,
        handlers=handlers,
        force=True,
    )

    # Create app logger
    logger = logging.getLogger("iris")
    logger.setLevel(getattr(logging, log_level, logging.INFO))
    logger.info("Logging configured successfully.")
