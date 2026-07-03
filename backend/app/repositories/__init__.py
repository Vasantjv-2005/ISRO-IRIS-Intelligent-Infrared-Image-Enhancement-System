"""
Repository Layer Package

Exports database repositories for all domain entities.
"""

from app.repositories.analysis_repository import (
    AnalysisRepository,
    analysis_repository,
)
from app.repositories.base_repository import BaseRepository
from app.repositories.comparison_repository import (
    ComparisonRepository,
    comparison_repository,
)
from app.repositories.dashboard_repository import (
    DashboardRepository,
    dashboard_repository,
)
from app.repositories.image_repository import (
    ImageRepository,
    image_repository,
)
from app.repositories.report_repository import (
    ReportRepository,
    report_repository,
)
from app.repositories.session_repository import (
    SessionRepository,
    session_repository,
)
from app.repositories.upload_repository import (
    UploadRepository,
    upload_repository,
)

__all__ = [
    "BaseRepository",
    "UploadRepository",
    "upload_repository",
    "SessionRepository",
    "session_repository",
    "AnalysisRepository",
    "analysis_repository",
    "ReportRepository",
    "report_repository",
    "ComparisonRepository",
    "comparison_repository",
    "DashboardRepository",
    "dashboard_repository",
    "ImageRepository",
    "image_repository",
]
