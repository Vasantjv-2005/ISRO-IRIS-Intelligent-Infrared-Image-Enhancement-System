"""
Report Controller

Handles PDF report generation requests by delegating to ReportGenerationService.
"""

from __future__ import annotations

from datetime import datetime

from app.schemas.report_schema import ReportRequestSchema, ReportResponseSchema
from app.services.ai.report_generation_service import report_generation_service


class ReportController:
    """
    Controller responsible for PDF report generation.
    """

    async def generate_report(
        self,
        request: ReportRequestSchema,
    ) -> ReportResponseSchema:
        """
        Generate a PDF report for a processed image.
        """
        report_path = report_generation_service.generate_report(
            report_path=f"reports/{request.image_name.split('.')[0]}_report.pdf",
            image_name=request.image_name,
            detected_objects=[
                detection.model_dump()
                for detection in request.detected_objects
            ],
            analysis=request.analysis,
        )

        return ReportResponseSchema(
            success=True,
            report_path=report_path,
            image_name=request.image_name,
            generated_at=datetime.utcnow().isoformat(),
            total_detected_objects=len(request.detected_objects),
            message="Report generated successfully.",
        )


report_controller = ReportController()
