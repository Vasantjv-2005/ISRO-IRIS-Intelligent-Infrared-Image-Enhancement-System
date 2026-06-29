"""
Application Router

Registers all API routes for the IRIS Backend.
"""

from fastapi import APIRouter

from app.api.routes.analysis import router as analysis_router
from app.api.routes.colorization import router as colorization_router
from app.api.routes.comparison import router as comparison_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.detection import router as detection_router
from app.api.routes.download import router as download_router
from app.api.routes.enhancement import router as enhancement_router
from app.api.routes.health import router as health_router
from app.api.routes.preprocessing import router as preprocessing_router
from app.api.routes.report import router as report_router
from app.api.routes.session import router as session_router
from app.api.routes.upload import router as upload_router

api_router = APIRouter()

# ---------------------------------------------------------
# System
# ---------------------------------------------------------

api_router.include_router(health_router)

# ---------------------------------------------------------
# Upload
# ---------------------------------------------------------

api_router.include_router(upload_router)

# ---------------------------------------------------------
# Image Processing
# ---------------------------------------------------------

api_router.include_router(preprocessing_router)
api_router.include_router(enhancement_router)
api_router.include_router(colorization_router)

# ---------------------------------------------------------
# AI Analysis
# ---------------------------------------------------------

api_router.include_router(detection_router)
api_router.include_router(analysis_router)

# ---------------------------------------------------------
# Reports
# ---------------------------------------------------------

api_router.include_router(report_router)

# ---------------------------------------------------------
# Dashboard
# ---------------------------------------------------------

api_router.include_router(comparison_router)
api_router.include_router(dashboard_router)

# ---------------------------------------------------------
# Session
# ---------------------------------------------------------

api_router.include_router(session_router)

# ---------------------------------------------------------
# Download
# ---------------------------------------------------------

api_router.include_router(download_router)