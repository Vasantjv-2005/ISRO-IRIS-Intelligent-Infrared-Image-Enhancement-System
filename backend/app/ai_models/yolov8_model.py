"""
YOLOv8 Model

Production-ready wrapper around the Ultralytics YOLOv8 model.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from ultralytics import YOLO

from app.core.config import YOLO_MODEL_PATH
from app.ai_models.utils import validate_weights
from app.middleware.error_handler import WeightsInvalidError

logger = logging.getLogger("iris")


class YOLOv8Model:
    """
    Wrapper around the Ultralytics YOLO model.
    """

    def __init__(
        self,
        model_path: str | Path | None = None,
    ) -> None:
        self.model_path = Path(model_path or YOLO_MODEL_PATH)
        self.model: YOLO | None = None

    # ---------------------------------------------------------
    # Load Model
    # ---------------------------------------------------------

    def load(self) -> None:
        """
        Load the YOLO model into memory.
        """
        if self.model is not None:
            return

        # Validate weights first to ensure it's not missing or a 0-byte placeholder
        validate_weights(self.model_path)

        try:
            self.model = YOLO(str(self.model_path))
        except Exception as e:
            logger.error(f"Failed to load YOLOv8 model from {self.model_path}: {e}")
            raise WeightsInvalidError(
                f"YOLO model file is invalid or corrupted: {e}"
            ) from e

    # ---------------------------------------------------------
    # Predict
    # ---------------------------------------------------------

    def predict(
        self,
        image_path: str,
        confidence: float = 0.25,
        save: bool = False,
        output_directory: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Run object detection.
        """
        self.load()

        assert self.model is not None

        image = Path(image_path)
        if not image.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        results = self.model.predict(
            source=str(image),
            conf=confidence,
            save=save,
            project=output_directory if save else None,
            exist_ok=True,
            verbose=False,
        )

        detections: list[dict[str, Any]] = []

        for result in results:
            names = result.names
            for box in result.boxes:
                coords = box.xyxy[0].tolist()
                detections.append(
                    {
                        "class_id": int(box.cls.item()),
                        "class_name": names[int(box.cls.item())],
                        "confidence": float(box.conf.item()),
                        "bbox": {
                            "x1": float(coords[0]),
                            "y1": float(coords[1]),
                            "x2": float(coords[2]),
                            "y2": float(coords[3]),
                        },
                    }
                )

        return detections

    # ---------------------------------------------------------
    # Model Information
    # ---------------------------------------------------------

    def info(self) -> dict[str, Any]:
        """
        Return model metadata.
        """
        self.load()

        return {
            "model_path": str(self.model_path),
            "loaded": self.model is not None,
        }

    # ---------------------------------------------------------
    # Unload
    # ---------------------------------------------------------

    def unload(self) -> None:
        """
        Release model from memory.
        """
        self.model = None


# -------------------------------------------------------------
# Singleton
# -------------------------------------------------------------

yolov8_model = YOLOv8Model()