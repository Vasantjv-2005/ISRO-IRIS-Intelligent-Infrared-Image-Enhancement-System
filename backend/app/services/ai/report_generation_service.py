"""
AI Report Generation Service

Generates PDF reports for processed infrared images and integrates
with the repository layer for status tracking and persistence.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

from app.middleware.error_handler import ReportGenerationException
from app.models.report_model import ReportModel, ReportStatus, utc_now
from app.repositories.report_repository import report_repository
from app.repositories.upload_repository import upload_repository
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


class ReportGenerationService:
    """
    Service responsible for generating PDF reports.
    """

    def generate_report(
        self,
        report_path: str,
        image_name: str,
        detected_objects: list[dict[str, Any]],
        analysis: str,
    ) -> str:
        """
        Generate a PDF report.

        Args:
            report_path: Output PDF path.
            image_name: Image filename.
            detected_objects: Objects detected by YOLO.
            analysis: Gemini-generated analysis.

        Returns:
            Path to generated report.
        """
        try:
            logger.info("Generating PDF report for image: %s at %s", image_name, report_path)
            output = Path(report_path)
            output.parent.mkdir(parents=True, exist_ok=True)

            document = SimpleDocTemplate(str(output))
            styles = getSampleStyleSheet()
            elements = []

            # Title
            elements.append(
                Paragraph(
                    "<b>IRIS Analysis Report</b>",
                    styles["Title"],
                )
            )
            elements.append(Spacer(1, 20))

            # Metadata
            elements.append(
                Paragraph(
                    f"<b>Image:</b> {image_name}",
                    styles["BodyText"],
                )
            )
            elements.append(
                Paragraph(
                    f"<b>Generated:</b> {utc_now()}",
                    styles["BodyText"],
                )
            )
            elements.append(Spacer(1, 20))

            # Detection Results
            elements.append(
                Paragraph(
                    "<b>Detected Objects</b>",
                    styles["Heading2"],
                )
            )

            if detected_objects:
                for obj in detected_objects:
                    elements.append(
                        Paragraph(
                            (
                                f"- {obj.get('class_name', 'unknown')} "
                                f"(Confidence: "
                                f"{float(obj.get('confidence', 0.0)):.2f})"
                            ),
                            styles["BodyText"],
                        )
                    )
            else:
                elements.append(
                    Paragraph(
                        "No objects detected.",
                        styles["BodyText"],
                    )
                )

            elements.append(Spacer(1, 20))

            # AI Analysis
            elements.append(
                Paragraph(
                    "<b>Gemini Analysis</b>",
                    styles["Heading2"],
                )
            )
            elements.append(
                Paragraph(
                    analysis.replace("\n", "<br/>"),
                    styles["BodyText"],
                )
            )

            document.build(elements)
            logger.info("Successfully generated report: %s", output)
            return str(output)

        except Exception as exc:
            logger.error("Failed to generate report %s: %s", report_path, exc, exc_info=True)
            raise ReportGenerationException(f"Failed to generate report: {exc}") from exc

    async def generate_report_async(
        self,
        report_path: str,
        image_name: str,
        detected_objects: list[dict[str, Any]],
        analysis: str,
        upload_id: str | None = None,
        analysis_id: str | None = None,
    ) -> str:
        """
        Generate a PDF report and persist metadata to the repositories.
        """
        res_path = self.generate_report(
            report_path=report_path,
            image_name=image_name,
            detected_objects=detected_objects,
            analysis=analysis,
        )

        if upload_id:
            try:
                file_size = Path(res_path).stat().st_size if Path(res_path).exists() else 0
                report_doc = ReportModel(
                    upload_id=upload_id,
                    analysis_id=analysis_id,
                    report_path=res_path,
                    status=ReportStatus.COMPLETED,
                    ai_summary=analysis[:200] + "..." if len(analysis) > 200 else analysis,
                    total_objects_detected=len(detected_objects),
                    report_size=file_size,
                    generated_at=utc_now(),
                )
                await report_repository.create(report_doc)
                await upload_repository.save_report_path(
                    upload_id=upload_id,
                    report_path=res_path,
                )
                logger.info("Persisted report metadata to database for upload: %s", upload_id)
            except Exception as exc:
                logger.warning("Failed to save report metadata to DB for upload %s: %s", upload_id, exc)

        return res_path


report_generation_service = ReportGenerationService()