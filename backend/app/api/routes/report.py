"""
Report Routes

API endpoints for PDF report generation.
"""

from datetime import datetime

from fastapi import APIRouter, HTTPException, status

from app.middleware.error_handler import ReportGenerationException
from app.schemas.report_schema import (
    ReportRequestSchema,
    ReportResponseSchema,
)
from app.controllers.report_controller import report_controller

router = APIRouter(
    prefix="/report",
    tags=["AI Report"],
)


@router.post(
    "/generate",
    response_model=ReportResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Generate PDF Report",
)
async def generate_report(
    request: ReportRequestSchema,
) -> ReportResponseSchema:
    """
    Generate a PDF report for a processed image.
    """

    try:

        return await report_controller.generate_report(request)

    except ReportGenerationException as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=exc.message,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )