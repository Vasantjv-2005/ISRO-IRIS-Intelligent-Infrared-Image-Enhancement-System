"""
AI Report Generation Service

Generates PDF reports for processed infrared images.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

from app.middleware.error_handler import ReportGenerationException


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
            report_path:
                Output PDF path.

            image_name:
                Image filename.

            detected_objects:
                Objects detected by YOLO.

            analysis:
                Gemini-generated analysis.

        Returns:
            Path to generated report.
        """

        try:

            output = Path(report_path)

            output.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            document = SimpleDocTemplate(
                str(output)
            )

            styles = getSampleStyleSheet()

            elements = []

            # ---------------------------------
            # Title
            # ---------------------------------

            elements.append(
                Paragraph(
                    "<b>IRIS Analysis Report</b>",
                    styles["Title"],
                )
            )

            elements.append(Spacer(1, 20))

            # ---------------------------------
            # Metadata
            # ---------------------------------

            elements.append(
                Paragraph(
                    f"<b>Image:</b> {image_name}",
                    styles["BodyText"],
                )
            )

            elements.append(
                Paragraph(
                    f"<b>Generated:</b> {datetime.utcnow()}",
                    styles["BodyText"],
                )
            )

            elements.append(Spacer(1, 20))

            # ---------------------------------
            # Detection Results
            # ---------------------------------

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
                                f"- {obj['class_name']} "
                                f"(Confidence: "
                                f"{obj['confidence']:.2f})"
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

            # ---------------------------------
            # AI Analysis
            # ---------------------------------

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

            return str(output)

        except Exception as exc:

            raise ReportGenerationException(
                f"Failed to generate report: {exc}"
            )


report_generation_service = ReportGenerationService()