"""
Pipeline Service

Orchestrates the end-to-end processing pipeline: image enhancement,
colorization, YOLOv8 object detection, Gemini scene analysis, PDF report
generation, and similarity comparison, while updating repositories.
"""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

from app.middleware.error_handler import ImageProcessingException
from app.models.upload_model import ProcessingStatus
from app.repositories.upload_repository import upload_repository
from app.schemas.pipeline_schema import PipelineRequestSchema, PipelineResponseSchema
from app.services.ai.analysis_service import analysis_service
from app.services.ai.colorization_service import colorization_service
from app.services.ai.detection_service import detection_service
from app.services.ai.enhancement_service import enhancement_service
from app.services.ai.report_generation_service import report_generation_service
from app.services.dashboard.comparison_service import comparison_service
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


class PipelineService:
    """
    Orchestrator service for end-to-end infrared image processing.
    """

    async def run_pipeline(
        self,
        request: PipelineRequestSchema,
        upload_id: str | None = None,
    ) -> PipelineResponseSchema:
        """
        Execute the full processing pipeline on an infrared image.

        Args:
            request: Pipeline Request parameters including image_path and confidence.
            upload_id: Optional upload ID to link repository updates.

        Returns:
            PipelineResponseSchema containing all output paths and analysis.
        """
        try:
            input_file = Path(request.image_path)
            if not input_file.exists():
                raise FileNotFoundError(f"Input image not found: {request.image_path}")

            if not upload_id:
                upload_id = f"pipe_{uuid.uuid4().hex[:8]}"

            logger.info("Starting end-to-end pipeline processing for upload: %s", upload_id)
            await upload_repository.update_status(upload_id, ProcessingStatus.PREPROCESSING)

            base_out = Path(request.output_directory)
            enhanced_dir = base_out / "enhanced"
            colorized_dir = base_out / "colorized"
            detection_dir = base_out / "detections"
            report_dir = base_out / "reports"

            for folder in (enhanced_dir, colorized_dir, detection_dir, report_dir):
                folder.mkdir(parents=True, exist_ok=True)

            # Step 1: Enhancement
            enhanced_path = str(enhanced_dir / f"enhanced_{input_file.name}")
            enhancement_service.enhance(
                input_path=request.image_path,
                output_path=enhanced_path,
            )
            await upload_repository.save_enhancement_path(upload_id, enhanced_path)
            await upload_repository.update_status(upload_id, ProcessingStatus.ENHANCED)
            logger.info("Pipeline Step 1 (Enhancement) completed for: %s", upload_id)

            # Step 2: Colorization
            colorized_path = str(colorized_dir / f"colorized_{input_file.name}")
            colorization_service.colorize(
                input_path=enhanced_path,
                output_path=colorized_path,
            )
            await upload_repository.save_colorization_path(upload_id, colorized_path)
            await upload_repository.update_status(upload_id, ProcessingStatus.COLORIZED)
            logger.info("Pipeline Step 2 (Colorization) completed for: %s", upload_id)

            # Step 3: Detection
            detection_res = detection_service.detect(
                image_path=colorized_path,
                output_directory=str(detection_dir),
                confidence=request.confidence,
            )
            detections = detection_res.get("detections", [])
            await upload_repository.save_detection_results(upload_id, detections)
            await upload_repository.update_status(upload_id, ProcessingStatus.DETECTED)
            logger.info("Pipeline Step 3 (Detection) completed with %d objects for: %s", len(detections), upload_id)

            # Step 4: AI Analysis
            await upload_repository.update_status(upload_id, ProcessingStatus.ANALYZED)
            analysis_res = await analysis_service.analyze_async(
                detected_objects=detections,
                image_name=input_file.name,
                upload_id=upload_id,
            )
            analysis_text = str(analysis_res.get("analysis", ""))
            logger.info("Pipeline Step 4 (AI Analysis) completed for: %s", upload_id)

            # Step 5: Report Generation
            report_path = str(report_dir / f"report_{input_file.stem}.pdf")
            await report_generation_service.generate_report_async(
                report_path=report_path,
                image_name=input_file.name,
                detected_objects=detections,
                analysis=analysis_text,
                upload_id=upload_id,
            )
            logger.info("Pipeline Step 5 (Report Generation) completed for: %s", upload_id)

            # Step 6: Comparison
            try:
                if await upload_repository.exists(upload_id):
                    await comparison_service.compare(db=None, upload_id=upload_id)
            except Exception as comp_exc:
                logger.warning("Pipeline comparison step skipped or failed for %s: %s", upload_id, comp_exc)

            # Mark upload as COMPLETED
            await upload_repository.update_status(upload_id, ProcessingStatus.COMPLETED)
            logger.info("End-to-end pipeline completed successfully for: %s", upload_id)

            return PipelineResponseSchema(
                success=True,
                upload_id=upload_id,
                processed_image=request.image_path,
                enhanced_image=enhanced_path,
                colorized_image=colorized_path,
                detection_count=len(detections),
                analysis=analysis_text,
                report_path=report_path,
                message="Pipeline processing completed successfully.",
            )

        except Exception as exc:
            logger.error("Pipeline execution failed for upload %s: %s", upload_id, exc, exc_info=True)
            if upload_id:
                await upload_repository.mark_as_failed(upload_id, str(exc))
            raise ImageProcessingException(f"Pipeline execution failed: {exc}") from exc


pipeline_service = PipelineService()
