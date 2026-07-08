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
from app.services.image_processing.preprocessing_service import preprocessing_service
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


class PipelineService:
    """
    Orchestrator service for end-to-end infrared image processing.
    """

    async def _update_session_progress(self, upload_id: str, progress: int, stage_name: str) -> None:
        """Helper to update session state in MongoDB."""
        try:
            from app.repositories.session_repository import session_repository
            from app.services.session.session_service import session_service
            sess = await session_repository.get_by_upload_id(upload_id)
            if sess:
                await session_service.update_progress(
                    db=None,
                    session_id=sess.session_id,
                    progress=progress,
                    current_stage=stage_name,
                )
        except Exception as exc:
            logger.warning("Failed to update session progress for stage %s (%s): %s", stage_name, upload_id, exc)

    async def run_pipeline(
        self,
        request: PipelineRequestSchema,
        upload_id: str | None = None,
    ) -> PipelineResponseSchema:
        """
        Execute the full processing pipeline on an infrared image sequentially.

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

            logger.info("Starting end-to-end sequential pipeline processing for upload: %s", upload_id)
            await upload_repository.update_status(upload_id, ProcessingStatus.PREPROCESSING)

            base_out = Path(request.output_directory)
            preprocessing_dir = base_out / "preprocessing"
            enhanced_dir = base_out / "enhanced"
            colorized_dir = base_out / "colorized"
            detection_dir = base_out / "detected"
            analyzed_dir = base_out / "analyzed"
            report_dir = base_out / "reports"

            for folder in (preprocessing_dir, enhanced_dir, colorized_dir, detection_dir, analyzed_dir, report_dir):
                folder.mkdir(parents=True, exist_ok=True)

            # Stage 1: Preprocessing (consumes uploaded image)
            preproc_res = preprocessing_service.process(
                input_path=request.image_path,
                output_directory=str(preprocessing_dir),
                apply_crop=False,
            )
            preprocessed_path = str(preproc_res.get("output_path") or preproc_res.get("processed_image") or (preprocessing_dir / input_file.name))
            await upload_repository.save_preprocessing_path(upload_id, preprocessed_path)
            await upload_repository.update_status(upload_id, ProcessingStatus.PREPROCESSING)
            await self._update_session_progress(upload_id, 15, "Preprocessing")
            logger.info("Pipeline Stage 1 (Preprocessing) completed for %s: %s", upload_id, preprocessed_path)

            # Stage 2: Enhancement (consumes preprocessed image)
            enhanced_path = str(enhanced_dir / input_file.name)
            enhanced_path = enhancement_service.enhance(
                input_path=preprocessed_path,
                output_path=enhanced_path,
            )
            await upload_repository.save_enhancement_path(upload_id, enhanced_path)
            await upload_repository.update_status(upload_id, ProcessingStatus.ENHANCED)
            await self._update_session_progress(upload_id, 30, "Enhancement")
            logger.info("Pipeline Stage 2 (Enhancement) completed for %s: %s", upload_id, enhanced_path)

            # Stage 3: YOLO Object Detection (runs STRICTLY on enhanced grayscale infrared image)
            detection_res = detection_service.detect(
                image_path=enhanced_path,
                output_directory=str(detection_dir),
                confidence=request.confidence,
            )
            detections = detection_res.get("detections", [])
            detected_path = str(detection_res.get("output_path") or (detection_dir / input_file.name))
            await upload_repository.save_detection_results(upload_id, detections, detected_path=detected_path)
            await upload_repository.update_status(upload_id, ProcessingStatus.DETECTED)
            await self._update_session_progress(upload_id, 55, "Object Detection")
            logger.info("Pipeline Stage 3 (Detection) completed with %d objects for %s: %s", len(detections), upload_id, detected_path)

            # Stage 4: Gemini AI Analysis (consumes YOLO detections and enhanced/detected image)
            await upload_repository.update_status(upload_id, ProcessingStatus.ANALYZED)
            analysis_res = await analysis_service.analyze_async(
                detected_objects=detections,
                image_name=input_file.name,
                upload_id=upload_id,
                output_directory=str(analyzed_dir),
                input_image_path=detected_path,
            )
            analysis_text = str(analysis_res.get("analysis", ""))
            analyzed_path = str(analysis_res.get("output_path") or (analyzed_dir / input_file.name))
            await self._update_session_progress(upload_id, 75, "AI Analysis")
            logger.info("Pipeline Stage 4 (AI Analysis) completed for %s: %s", upload_id, analyzed_path)

            # Stage 5: Natural AI Colorization (STRICTLY FOR VISUALIZATION - Never input to YOLO)
            colorized_path = str(colorized_dir / input_file.name)
            cmap_arg = getattr(request, "color_map", "inferno")
            colorized_path = colorization_service.colorize(
                input_path=enhanced_path,
                output_path=colorized_path,
                color_map=cmap_arg,
            )
            await upload_repository.save_colorization_path(upload_id, colorized_path)
            await upload_repository.update_status(upload_id, ProcessingStatus.COLORIZED)
            await self._update_session_progress(upload_id, 88, "Colorization")
            logger.info("Pipeline Stage 5 (Colorization for visualization) completed for %s: %s", upload_id, colorized_path)

            # Stage 6: PDF Report Generation (includes Original, Enhanced, Detected Images + Bounding Boxes + Analysis)
            report_path = str(report_dir / f"report_{input_file.stem}.pdf")
            await report_generation_service.generate_report_async(
                report_path=report_path,
                image_name=input_file.name,
                detected_objects=detections,
                analysis=analysis_text,
                upload_id=upload_id,
                original_image_path=raw_path,
                enhanced_image_path=enhanced_path,
                detected_image_path=detected_path,
                processing_time=time.time() - start_time,
                model_info={
                    "yolo": "YOLOv8 Infrared Scene Detection Engine",
                    "colorization": "Natural Daylight AI Colorization",
                    "enhancement": "CLAHE + Multiscale Infrared Super-Resolution",
                    "analysis": "Google Gemini Scientific Scene Interpreter",
                },
            )
            await self._update_session_progress(upload_id, 95, "Report Generation")
            logger.info("Pipeline Stage 6 (Report Generation) completed for %s: %s", upload_id, report_path)

            # Stage 7: Comparison
            try:
                if await upload_repository.exists(upload_id):
                    await comparison_service.compare(db=None, upload_id=upload_id)
            except Exception as comp_exc:
                logger.warning("Pipeline comparison stage skipped or failed for %s: %s", upload_id, comp_exc)

            # Mark upload and session as COMPLETED
            await upload_repository.update_status(upload_id, ProcessingStatus.COMPLETED)
            await self._update_session_progress(upload_id, 100, "Completed")
            logger.info("End-to-end sequential pipeline completed successfully for: %s", upload_id)

            return PipelineResponseSchema(
                success=True,
                upload_id=upload_id,
                processed_image=request.image_path,
                preprocessed_image=preprocessed_path,
                enhanced_image=enhanced_path,
                colorized_image=colorized_path,
                detected_image=detected_path,
                analyzed_image=analyzed_path,
                detection_count=len(detections),
                analysis=analysis_text,
                report_path=report_path,
                message="Pipeline processing completed successfully.",
            )

        except Exception as exc:
            logger.error("Pipeline execution failed for upload %s: %s", upload_id, exc, exc_info=True)
            if upload_id:
                await upload_repository.mark_as_failed(upload_id, str(exc))
                await self._update_session_progress(upload_id, 0, f"Failed: {exc}")
            raise ImageProcessingException(f"Pipeline execution failed: {exc}") from exc


pipeline_service = PipelineService()
