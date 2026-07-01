"""
Application Constants
"""

from __future__ import annotations

# General
PROJECT_NAME = "IRIS"
VERSION = "1.0.0"

# Timeouts & Limits
MAX_UPLOAD_SIZE_BYTES = 20 * 1024 * 1024  # 20MB

# Supported Formats
SUPPORTED_IMAGE_FORMATS = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/tiff": ".tiff",
    "image/tif": ".tif",
}

# Directories
DEFAULT_OUTPUT_DIR = "outputs"
DEFAULT_REPORTS_DIR = "reports"
