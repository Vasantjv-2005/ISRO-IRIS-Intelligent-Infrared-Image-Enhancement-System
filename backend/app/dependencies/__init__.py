"""
Dependency Injection Package

Exports reusable dependency providers for the
IRIS Backend.
"""

from app.dependencies.ai import (
    get_analysis_service,
    get_colorization_service,
    get_detection_service,
    get_enhancement_service,
    get_report_generation_service,
)
from app.dependencies.database import get_database
from app.dependencies.upload import get_upload_service

__all__ = [
    "get_database",
    "get_upload_service",
    "get_enhancement_service",
    "get_colorization_service",
    "get_detection_service",
    "get_analysis_service",
    "get_report_generation_service",
]