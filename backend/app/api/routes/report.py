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
from app.services.ai.report_generation_service import (
    report_generation_service,
)

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

        report_path = (
            report_generation_service.generate_report(
                report_path=f"reports/{request.image_name.split('.')[0]}_report.pdf",
                image_name=request.image_name,
                detected_objects=[
                    detection.model_dump()
                    for detection in request.detected_objects
                ],
                analysis=request.analysis,
            )
        )

        return ReportResponseSchema(
            success=True,
            report_path=report_path,
            image_name=request.image_name,
            generated_at=datetime.utcnow().isoformat(),
            total_detected_objects=len(
                request.detected_objects
            ),
            message="Report generated successfully.",
        )

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