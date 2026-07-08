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
        original_image_path: str | None = None,
        enhanced_image_path: str | None = None,
        detected_image_path: str | None = None,
        processing_time: float | None = None,
        model_info: dict[str, Any] | str | None = None,
    ) -> str:
        """
        Generate a PDF report.

        Args:
            report_path: Output PDF path.
            image_name: Image filename.
            detected_objects: Objects detected by YOLO.
            analysis: Gemini-generated analysis.
            original_image_path: Optional original image path.
            enhanced_image_path: Optional enhanced image path.
            detected_image_path: Optional detected image path.
            processing_time: Optional processing duration.
            model_info: Optional model metadata.

        Returns:
            Path to generated report.
        """
        try:
            logger.info("Generating PDF report for image: %s at %s", image_name, report_path)
            output = Path(report_path)
            output.parent.mkdir(parents=True, exist_ok=True)

            from reportlab.lib import colors
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import (
                Image,
                Paragraph,
                SimpleDocTemplate,
                Spacer,
                Table,
                TableStyle,
            )

            document = SimpleDocTemplate(
                str(output),
                pagesize=letter,
                leftMargin=0.65 * inch,
                rightMargin=0.65 * inch,
                topMargin=0.65 * inch,
                bottomMargin=0.65 * inch,
            )
            styles = getSampleStyleSheet()

            # Custom beautiful color styles
            title_style = ParagraphStyle(
                "ExecutiveTitle",
                parent=styles["Title"],
                fontName="Helvetica-Bold",
                fontSize=20,
                leading=24,
                textColor=colors.HexColor("#FFFFFF"),
                alignment=1,
            )
            subtitle_style = ParagraphStyle(
                "ExecutiveSubtitle",
                parent=styles["Normal"],
                fontName="Helvetica",
                fontSize=11,
                leading=14,
                textColor=colors.HexColor("#E2E8F0"),
                alignment=1,
            )
            section_title_style = ParagraphStyle(
                "SectionHeading",
                parent=styles["Heading2"],
                fontName="Helvetica-Bold",
                fontSize=14,
                leading=18,
                textColor=colors.HexColor("#1E293B"),
                spaceAfter=8,
            )
            body_style = ParagraphStyle(
                "CustomBody",
                parent=styles["BodyText"],
                fontName="Helvetica",
                fontSize=10,
                leading=14,
                textColor=colors.HexColor("#334155"),
            )
            table_header_style = ParagraphStyle(
                "TableHeader",
                parent=styles["Normal"],
                fontName="Helvetica-Bold",
                fontSize=9,
                leading=12,
                textColor=colors.HexColor("#FFFFFF"),
                alignment=1,
            )
            table_cell_style = ParagraphStyle(
                "TableCell",
                parent=styles["Normal"],
                fontName="Helvetica",
                fontSize=9,
                leading=12,
                textColor=colors.HexColor("#1E293B"),
            )

            elements = []

            # 1. Executive Header Banner Table
            header_table_data = [
                [
                    Paragraph(
                        "<b>IRIS INTELLIGENT INFRARED AI ENHANCEMENT & DETECTION REPORT</b>",
                        title_style,
                    )
                ],
                [
                    Paragraph(
                        f"Image: <b>{image_name}</b> &nbsp;|&nbsp; Generated: <b>{utc_now().strftime('%Y-%m-%d %H:%M:%S UTC')}</b>",
                        subtitle_style,
                    )
                ],
            ]
            header_table = Table(header_table_data, colWidths=[7.2 * inch])
            header_table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#1E293B")),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 4),
                    ("TOPPADDING", (0, 0), (-1, 0), 12),
                    ("BOTTOMPADDING", (0, 1), (-1, 1), 12),
                    ("TOPPADDING", (0, 1), (-1, 1), 4),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("LINEBELOW", (0, 1), (-1, 1), 3, colors.HexColor("#DC2626")),
                ])
            )
            elements.append(header_table)
            elements.append(Spacer(1, 18))

            # Optional Model Information Table block
            if model_info:
                if isinstance(model_info, dict):
                    minfo_str = " | ".join(f"<b>{k.upper()}</b>: {v}" for k, v in model_info.items())
                else:
                    minfo_str = str(model_info)
                minfo_table = Table(
                    [[Paragraph(f"<b>MODEL PIPELINE</b>: {minfo_str}", body_style)]],
                    colWidths=[7.2 * inch],
                )
                minfo_table.setStyle(
                    TableStyle([
                        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
                        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                        ("TOPPADDING", (0, 0), (-1, -1), 6),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                        ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ])
                )
                elements.append(minfo_table)
                elements.append(Spacer(1, 14))

            # 2. Multi-Image Visual Analysis Section
            img_stem = Path(image_name).stem
            detection_folder = Path("outputs/detections")

            orig_embed = original_image_path if (original_image_path and Path(original_image_path).exists()) else None
            enh_embed = enhanced_image_path if (enhanced_image_path and Path(enhanced_image_path).exists()) else None
            det_embed = detected_image_path if (detected_image_path and Path(detected_image_path).exists()) else None

            if not det_embed:
                candidates = [
                    detection_folder / image_name,
                    detection_folder / f"{img_stem}.jpg",
                ]
                for cand in candidates:
                    if cand.exists():
                        det_embed = str(cand)
                        break

            images_to_show = []
            if orig_embed:
                images_to_show.append(("ORIGINAL INFRARED IMAGE", orig_embed))
            if enh_embed:
                images_to_show.append(("ENHANCED INFRARED IMAGE", enh_embed))
            if det_embed:
                images_to_show.append(("YOLO DETECTION WITH BOUNDING BOXES", det_embed))

            if images_to_show:
                elements.append(
                    Paragraph("<b>VISUAL PHOTOGRAPH & OBJECT DETECTIONS</b>", section_title_style)
                )
                elements.append(Spacer(1, 6))
                for label, ipath in images_to_show:
                    elements.append(Paragraph(f"<b>{label}</b>", body_style))
                    elements.append(Spacer(1, 4))
                    img_flow = Image(ipath, width=5.2 * inch, height=3.3 * inch)
                    img_flow.hAlign = "CENTER"
                    elements.append(img_flow)
                    elements.append(Spacer(1, 10))
                elements.append(Spacer(1, 8))

            # 3. Comprehensive Categorized Detected Objects Inventory (Zero Hardcoding)
            elements.append(Paragraph("<b>DETECTED OBJECTS TABLE</b>", section_title_style))
            elements.append(Spacer(1, 6))

            table_data = [
                [
                    Paragraph("<b>#</b>", table_header_style),
                    Paragraph("<b>DETECTED OBJECT</b>", table_header_style),
                    Paragraph("<b>CONFIDENCE</b>", table_header_style),
                    Paragraph("<b>BOUNDING BOX (x1, y1, x2, y2)</b>", table_header_style),
                ]
            ]

            table_styles = [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E293B")),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("BOX", (0, 0), (-1, -1), 1.0, colors.HexColor("#475569")),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]

            if not detected_objects:
                table_data.append([
                    Paragraph("-", table_cell_style),
                    Paragraph("No discrete thermal objects detected", table_cell_style),
                    Paragraph("N/A", table_cell_style),
                    Paragraph("N/A", table_cell_style),
                ])
                table_styles.append(("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#FFFFFF")))
            else:
                for idx, obj in enumerate(detected_objects, 1):
                    cname = str(obj.get("class_name", "OBJECT")).upper()
                    conf = float(obj.get("confidence", 0.0))
                    bbox_dict = obj.get("bbox", {})
                    if isinstance(bbox_dict, dict) and "x1" in bbox_dict:
                        bbox_str = f"({int(bbox_dict.get('x1', 0))}, {int(bbox_dict.get('y1', 0))}, {int(bbox_dict.get('x2', 0))}, {int(bbox_dict.get('y2', 0))})"
                    else:
                        bbox_str = str(bbox_dict or "N/A")

                    row_bg = colors.HexColor("#F8FAFC") if idx % 2 == 1 else colors.HexColor("#FFFFFF")
                    table_data.append([
                        Paragraph(str(idx), table_cell_style),
                        Paragraph(f"<b>{cname}</b>", table_cell_style),
                        Paragraph(f"{conf * 100:.1f}%", table_cell_style),
                        Paragraph(bbox_str, table_cell_style),
                    ])
                    table_styles.append(("BACKGROUND", (0, idx), (-1, idx), row_bg))

            obj_table = Table(table_data, colWidths=[0.5 * inch, 2.0 * inch, 1.5 * inch, 3.2 * inch])
            obj_table.setStyle(TableStyle(table_styles))
            elements.append(obj_table)
            elements.append(Spacer(1, 18))

            # 4. Gemini AI Expert Analysis Block
            elements.append(Paragraph("<b>GEMINI AI SCENE INTERPRETATION & RISK ASSESSMENT</b>", section_title_style))
            elements.append(Spacer(1, 6))

            analysis_block_data = [[
                Paragraph(
                    analysis.replace("\n", "<br/>"),
                    body_style,
                )
            ]]
            analysis_table = Table(analysis_block_data, colWidths=[7.2 * inch])
            analysis_table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
                    ("BOX", (0, 0), (-1, -1), 1.0, colors.HexColor("#CBD5E1")),
                    ("LINELEFT", (0, 0), (0, -1), 4.0, colors.HexColor("#3B82F6")),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ])
            )
            elements.append(analysis_table)

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
        original_image_path: str | None = None,
        enhanced_image_path: str | None = None,
        detected_image_path: str | None = None,
        processing_time: float | None = None,
        model_info: dict[str, Any] | str | None = None,
    ) -> str:
        """
        Generate a PDF report and persist metadata to the repositories.
        """
        res_path = self.generate_report(
            report_path=report_path,
            image_name=image_name,
            detected_objects=detected_objects,
            analysis=analysis,
            original_image_path=original_image_path,
            enhanced_image_path=enhanced_image_path,
            detected_image_path=detected_image_path,
            processing_time=processing_time,
            model_info=model_info,
        )

        target_upload_id = upload_id or image_name
        try:
            file_size = Path(res_path).stat().st_size if Path(res_path).exists() else 0
            report_doc = ReportModel(
                upload_id=target_upload_id,
                analysis_id=analysis_id,
                report_path=res_path,
                status=ReportStatus.COMPLETED,
                ai_summary=analysis[:200] + "..." if len(analysis) > 200 else analysis,
                total_objects_detected=len(detected_objects),
                report_size=file_size,
                generated_at=utc_now(),
            )
            await report_repository.create(report_doc)
            if upload_id:
                await upload_repository.save_report_path(
                    upload_id=upload_id,
                    report_path=res_path,
                )
            logger.info("Persisted report metadata to database for upload: %s", target_upload_id)
        except Exception as exc:
            logger.error("Failed to save report metadata to DB for upload %s: %s", target_upload_id, exc, exc_info=True)

        return res_path


report_generation_service = ReportGenerationService()