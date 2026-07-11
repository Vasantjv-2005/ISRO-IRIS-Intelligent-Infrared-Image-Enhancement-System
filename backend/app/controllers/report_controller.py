"""
Report Controller

Handles PDF report generation requests by delegating to ReportGenerationService.
"""

from __future__ import annotations

from datetime import datetime

from app.schemas.report_schema import ReportRequestSchema, ReportResponseSchema
from app.services.ai.report_generation_service import report_generation_service


from app.repositories.upload_repository import upload_repository


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
        target_upload_id = getattr(request, "upload_id", None)
        doc = None
        try:
            if target_upload_id:
                doc = await upload_repository.get_by_upload_id(target_upload_id)
            if not doc:
                doc = await upload_repository.get_by_filename(request.image_name)
        except Exception:
            pass

        detected_objs = [detection.model_dump() for detection in request.detected_objects]
        if doc and doc.objects_detected:
            detected_objs = doc.objects_detected

        orig_path = getattr(request, "original_image_path", None)
        enh_path = getattr(request, "processed_image_path", None)
        col_path = getattr(request, "colorized_image_path", None)
        det_path = getattr(request, "detected_image_path", None)

        if doc:
            orig_path = orig_path or doc.raw_path or getattr(doc, "filepath", None)
            enh_path = enh_path or doc.enhanced_path
            col_path = col_path or doc.colorized_path
            det_path = det_path or doc.detected_path

        report_path = await report_generation_service.generate_report_async(
            report_path=f"reports/{request.image_name.split('.')[0]}_report.pdf",
            image_name=request.image_name,
            detected_objects=detected_objs,
            analysis=request.analysis,
            upload_id=target_upload_id or request.image_name,
            original_image_path=orig_path,
            enhanced_image_path=enh_path,
            colorized_image_path=col_path,
            detected_image_path=det_path,
        )

        return ReportResponseSchema(
            success=True,
            report_path=report_path,
            image_name=request.image_name,
            generated_at=datetime.utcnow().isoformat(),
            total_detected_objects=len(detected_objs),
            message="Report generated successfully.",
        )


report_controller = ReportController()
