"""
AI Detection Service

Performs object detection on infrared images using YOLOv8.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ultralytics import YOLO

from app.core.settings import settings
from app.middleware.error_handler import ImageProcessingException


class DetectionService:
    """
    Service responsible for object detection.
    """

    def __init__(self) -> None:
        self.model: YOLO | None = None

    def load_model(self) -> None:
        """
        Load the YOLO model only once.
        """

        if self.model is not None:
            return

        model_path = Path(settings.YOLO_MODEL_PATH)

        if not model_path.exists():
            raise ImageProcessingException(
                f"YOLO model not found: {model_path}"
            )

        self.model = YOLO(str(model_path))

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

        self.load_model()

        image = Path(image_path)

        if not image.exists():
            raise ImageProcessingException(
                "Input image not found."
            )

        results = self.model.predict(
            source=str(image),
            conf=confidence,
            save=True,
            project=output_directory,
            name="detections",
            exist_ok=True,
            verbose=False,
        )

        detections: list[dict[str, Any]] = []

        for result in results:

            for box in result.boxes:

                detections.append(
                    {
                        "class_id": int(box.cls[0]),
                        "class_name": self.model.names[
                            int(box.cls[0])
                        ],
                        "confidence": float(box.conf[0]),
                        "bbox": [
                            float(value)
                            for value in box.xyxy[0]
                        ],
                    }
                )

        return {
            "success": True,
            "image_path": image_path,
            "output_directory": output_directory,
            "total_objects": len(detections),
            "detections": detections,
        }


detection_service = DetectionService()