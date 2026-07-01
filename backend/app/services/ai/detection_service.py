"""
AI Detection Service

Performs object detection on infrared images using YOLOv8,
delegating loading and predictions to the unified YOLOv8Model wrapper.
"""

from __future__ import annotations

from typing import Any

from app.ai_models.yolov8_model import yolov8_model
from app.middleware.error_handler import ImageProcessingException


class DetectionService:
    """
    Service responsible for object detection.
    """

    def load_model(self) -> None:
        """
        Load the YOLO model only once.
        """
        try:
            yolov8_model.load()
        except Exception as exc:
            raise ImageProcessingException(
                f"Failed to load detection model: {exc}"
            ) from exc

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
            # Let yolov8_model handle prediction and coordinates format
            detections = yolov8_model.predict(
                image_path=image_path,
                confidence=confidence,
                save=True,
                output_directory=output_directory,
            )

            return {
                "success": True,
                "image_path": image_path,
                "output_directory": output_directory,
                "total_objects": len(detections),
                "detections": detections,
            }
        except Exception as exc:
            raise ImageProcessingException(
                f"Detection execution failed: {exc}"
            ) from exc


detection_service = DetectionService()