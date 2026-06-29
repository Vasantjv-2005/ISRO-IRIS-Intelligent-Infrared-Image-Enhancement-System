"""
Report Routes

API endpoints for generating PDF reports.
"""

from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

from app.middleware.error_handler import ReportGenerationException
from app.services.ai.report_generation_service import (
    report_generation_service,
)

router = APIRouter(
    prefix="/report",
    tags=["AI Report"],
)


@router.post(
    "/generate",
    summary="Generate AI Report",
)
async def generate_report(
    image_name: str,
    detected_objects: list[dict[str, Any]],
    analysis: str,
):
    """
    Generate a PDF report.
    """

    try:

        reports_directory = Path("reports")

        reports_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        report_path = reports_directory / (
            f"{Path(image_name).stem}_report.pdf"
        )

        generated_report = (
            report_generation_service.generate_report(
                report_path=str(report_path),
                image_name=image_name,
                detected_objects=detected_objects,
                analysis=analysis,
            )
        )

        return {
            "success": True,
            "message": "Report generated successfully.",
            "report_path": generated_report,
        }

    except ReportGenerationException as exc:

        raise HTTPException(
            status_code=500,
            detail=exc.message,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )