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

            from pathlib import Path
            output_dir = Path(output_directory)
            output_dir.mkdir(parents=True, exist_ok=True)
            input_file = Path(image_path)
            output_file = output_dir / input_file.name

            yolo_saved = output_dir / "predict" / input_file.name
            if yolo_saved.exists() and yolo_saved != output_file:
                import shutil
                shutil.copy(str(yolo_saved), str(output_file))
            elif not output_file.exists() and input_file.exists():
                import cv2
                img = cv2.imread(str(input_file))
                if img is not None:
                    for det in detections:
                        bbox = det.get("bbox", {})
                        x1, y1, x2, y2 = int(bbox.get("x1", 0)), int(bbox.get("y1", 0)), int(bbox.get("x2", 0)), int(bbox.get("y2", 0))
                        label = f"{det.get('class_name', 'obj')} {det.get('confidence', 0.0):.2f}"
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        cv2.putText(img, label, (x1, max(y1 - 5, 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                    cv2.imwrite(str(output_file), img)

            return {
                "success": True,
                "image_path": image_path,
                "output_directory": output_directory,
                "output_path": str(output_file),
                "total_objects": len(detections),
                "detections": detections,
            }
        except Exception as exc:
            logger.error("Detection execution failed for %s: %s", image_path, exc, exc_info=True)
            raise ImageProcessingException(f"Detection execution failed: {exc}") from exc


detection_service = DetectionService()