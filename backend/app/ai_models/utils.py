"""
AI Model Utilities
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

from app.middleware.error_handler import (
    WeightsInvalidError,
    WeightsNotFoundError,
)

logger = logging.getLogger("iris")


def safe_import_torch():
    """
    Safely import torch and torch.nn, handling Windows DLL loading issues.
    """
    if sys.platform == "win32":
        try:
            import site
            for site_path in site.getsitepackages() + [site.getusersitepackages()]:
                torch_lib = os.path.join(site_path, "torch", "lib")
                if os.path.exists(torch_lib):
                    try:
                        os.add_dll_directory(torch_lib)
                    except Exception:
                        pass
        except Exception:
            pass
    try:
        import torch
        import torch.nn as nn
        return torch, nn, True
    except ImportError as e:
        logger.warning(f"PyTorch is not available or DLL failed to load ({e}). Using fallback backends.")
        return None, None, False


torch, nn, TORCH_AVAILABLE = safe_import_torch()


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
