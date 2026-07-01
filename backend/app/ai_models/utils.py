"""
AI Model Utilities
"""

from __future__ import annotations

import logging
from pathlib import Path

from app.middleware.error_handler import (
    WeightsInvalidError,
    WeightsNotFoundError,
)

logger = logging.getLogger("iris")


def validate_weights(path: Path) -> None:
    """
    Validate that model weights file exists and is not an empty/placeholder file.

    Args:
        path: Path to the weight file.

    Raises:
        WeightsNotFoundError: If the path does not exist.
        WeightsInvalidError: If the path is a directory or size is 0 bytes.
    """
    if not path.exists():
        raise WeightsNotFoundError(
            f"Model weights file not found at: {path.absolute()}"
        )

    if not path.is_file():
        raise WeightsInvalidError(
            f"Weights path is not a file: {path.absolute()}"
        )

    if path.stat().st_size == 0:
        raise WeightsInvalidError(
            f"Weights file at {path.absolute()} is empty (0-byte placeholder). "
            "Please ensure actual model weights are downloaded."
        )
