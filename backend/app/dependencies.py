"""
IRIS Dependencies Compatibility Module
"""

from __future__ import annotations

from app.dependencies import (
    get_analysis_service,
    get_colorization_service,
    get_database,
    get_detection_service,
    get_enhancement_service,
    get_report_generation_service,
    get_upload_service,
)

__all__ = [
    "get_database",
    "get_upload_service",
    "get_enhancement_service",
    "get_colorization_service",
    "get_detection_service",
    "get_analysis_service",
    "get_report_generation_service",
]
