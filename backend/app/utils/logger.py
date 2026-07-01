"""
Logger Utility

Centralized logging configuration for the
IRIS Backend.
"""

from __future__ import annotations

import logging
import logging.handlers
from pathlib import Path


class Logger:
    """
    Central logger manager.
    """

    _configured = False

    @classmethod
    def configure(
        cls,
        log_directory: str = "logs",
        log_level: int = logging.INFO,
    ) -> None:
        """
        Configure application logging.
        """

        if cls._configured:
            return

        log_dir = Path(log_directory)

        log_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        formatter = logging.Formatter(
            fmt=(
                "%(asctime)s | "
                "%(levelname)-8s | "
                "%(name)s | "
                "%(message)s"
            ),
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # =====================================================
        # Console Handler
        # =====================================================

        console_handler = logging.StreamHandler()

        console_handler.setLevel(
            log_level
        )

        console_handler.setFormatter(
            formatter
        )

        # =====================================================
        # File Handler
        # =====================================================

        file_handler = (
            logging.handlers.RotatingFileHandler(
                filename=log_dir / "iris.log",
                maxBytes=10 * 1024 * 1024,
                backupCount=5,
                encoding="utf-8",
            )
        )

        file_handler.setLevel(
            log_level
        )

        file_handler.setFormatter(
            formatter
        )

        # =====================================================
        # Root Logger
        # =====================================================

        root_logger = logging.getLogger()

        root_logger.setLevel(
            log_level
        )

        root_logger.handlers.clear()

        root_logger.addHandler(
            console_handler
        )

        root_logger.addHandler(
            file_handler
        )

        cls._configured = True

    # =====================================================
    # Get Logger
    # =====================================================

    @staticmethod
    def get_logger(
        name: str,
    ) -> logging.Logger:
        """
        Return a logger instance.
        """

        if not Logger._configured:
            Logger.configure()

        return logging.getLogger(
            name
        )


# ==========================================================
# Configure Logger Automatically
# ==========================================================

Logger.configure()

logger = Logger.get_logger("IRIS")