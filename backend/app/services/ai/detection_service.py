"""
AI Detection Service

Performs object detection on infrared images using YOLOv8,
delegating loading and predictions to the unified YOLOv8Model wrapper.
"""

from __future__ import annotations

from typing import Any

from app.ai_models.yolov8_model import yolov8_model
from app.middleware.error_handler import ImageProcessingException
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


class DetectionService:
    """
    Service responsible for object detection.
    """

    def load_model(self) -> None:
        """
        Load the YOLO model only once.
        """
        try:
            logger.info("Loading YOLOv8 detection model...")
            yolov8_model.load()
            logger.info("Successfully loaded YOLOv8 detection model.")
        except Exception as exc:
            logger.error("Failed to load detection model: %s", exc, exc_info=True)
            raise ImageProcessingException(f"Failed to load detection model: {exc}") from exc

    def detect(
        self,
        image_path: str,
        output_directory: str,
        confidence: float = 0.25,
    ) -> dict[str, Any]:
        """
        Detect objects in an image.

        Args:
            image_path:
                Input image.

            output_directory:
                Directory where YOLO saves predictions.

            confidence:
                Minimum confidence threshold.

        Returns:
            Detection results.
        """
        try:
            logger.info("Detecting objects in %s with confidence threshold %f", image_path, confidence)
            detections = yolov8_model.predict(
                image_path=image_path,
                confidence=confidence,
                save=True,
                output_directory=output_directory,
            )
            logger.info("Detected %d objects in %s", len(detections), image_path)
            return {
                "success": True,
                "image_path": image_path,
                "output_directory": output_directory,
                "total_objects": len(detections),
                "detections": detections,
            }
        except Exception as exc:
            logger.error("Detection execution failed for %s: %s", image_path, exc, exc_info=True)
            raise ImageProcessingException(f"Detection execution failed: {exc}") from exc


detection_service = DetectionService()