"""
AI Dependencies

Provides reusable AI service dependencies for FastAPI.
"""

from app.services.ai.analysis_service import (
    AnalysisService,
    analysis_service,
)
from app.services.ai.colorization_service import (
    ColorizationService,
    colorization_service,
)
from app.services.ai.detection_service import (
    DetectionService,
    detection_service,
)
from app.services.ai.enhancement_service import (
    EnhancementService,
    enhancement_service,
)
from app.services.ai.report_generation_service import (
    ReportGenerationService,
    report_generation_service,
)


def get_analysis_service() -> AnalysisService:
    """
    Return the Analysis Service instance.
    """
    return analysis_service


def get_colorization_service() -> ColorizationService:
    """
    Return the Colorization Service instance.
    """
    return colorization_service


def get_detection_service() -> DetectionService:
    """
    Return the Detection Service instance.
    """
    return detection_service


def get_enhancement_service() -> EnhancementService:
    """
    Return the Enhancement Service instance.
    """
    return enhancement_service


def get_report_generation_service() -> ReportGenerationService:
    """
    Return the Report Generation Service instance.
    """
    return report_generation_service
