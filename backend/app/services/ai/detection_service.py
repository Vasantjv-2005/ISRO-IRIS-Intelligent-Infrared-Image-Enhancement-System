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
            import cv2
            output_dir = Path(output_directory)
            output_dir.mkdir(parents=True, exist_ok=True)
            input_file = Path(image_path)

            output_file = output_dir / input_file.name

            img = cv2.imread(str(input_file))
            if img is not None:
                h, w = img.shape[:2]
                font_scale = max(0.42, max(h, w) / 2200.0)
                font_thickness = 1
                line_thick = max(1, int(max(h, w) / 800.0))

                # Sleek professional BGR color palette for scientific infrared features
                color_palette = {
                    "BUILDING": (40, 60, 240),       # Vermilion/Red
                    "FACTORY": (40, 60, 240),        # Red
                    "CHIMNEY": (0, 140, 255),        # Orange
                    "SMOKE": (240, 230, 80),         # Cyan/Yellow
                    "PIPE": (255, 140, 0),           # Blue
                    "VEHICLE": (220, 40, 180),       # Magenta
                    "PERSON": (0, 220, 255),         # Yellow
                    "BRIDGE": (30, 160, 255),        # Amber
                    "WATER": (255, 190, 40),         # Azure
                    "RIVER": (255, 190, 40),         # Azure
                    "TREE": (60, 200, 100),          # Green
                    "ROAD": (180, 180, 180),         # Silver
                }

                for det in detections:
                    bbox = det.get("bbox", {})
                    x1 = max(0, int(bbox.get("x1", 0)))
                    y1 = max(0, int(bbox.get("y1", 0)))
                    x2 = min(w - 1, int(bbox.get("x2", 0)))
                    y2 = min(h - 1, int(bbox.get("y2", 0)))

                    cname = det.get("class_name", "OBJECT").upper()
                    box_color = color_palette.get(cname, (255, 160, 40))

                    # 1. Sleek thin bounding box (anti-aliased)
                    cv2.rectangle(img, (x1, y1), (x2, y2), box_color, line_thick, cv2.LINE_AA)

                    # 2. Precision HUD Corner Accents (crisp thin lines)
                    cw = max(8, min(x2 - x1, y2 - y1) // 8)
                    hud_thick = line_thick + 1
                    cv2.line(img, (x1, y1), (x1 + cw, y1), box_color, hud_thick, cv2.LINE_AA)
                    cv2.line(img, (x1, y1), (x1, y1 + cw), box_color, hud_thick, cv2.LINE_AA)
                    cv2.line(img, (x2, y1), (x2 - cw, y1), box_color, hud_thick, cv2.LINE_AA)
                    cv2.line(img, (x2, y1), (x2, y1 + cw), box_color, hud_thick, cv2.LINE_AA)
                    cv2.line(img, (x1, y2), (x1 + cw, y2), box_color, hud_thick, cv2.LINE_AA)
                    cv2.line(img, (x1, y2), (x1, y2 - cw), box_color, hud_thick, cv2.LINE_AA)
                    cv2.line(img, (x2, y2), (x2 - cw, y2), box_color, hud_thick, cv2.LINE_AA)
                    cv2.line(img, (x2, y2), (x2, y2 - cw), box_color, hud_thick, cv2.LINE_AA)

                    # 3. Clean compact label banner
                    conf_pct = int(det.get("confidence", 0.0) * 100)
                    label = f"{cname} {conf_pct}%"
                    (text_w, text_h), baseline = cv2.getTextSize(
                        label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness
                    )

                    label_y1 = max(0, y1 - text_h - baseline - 6)
                    label_y2 = y1 if y1 >= text_h + baseline + 6 else y1 + text_h + baseline + 6
                    cv2.rectangle(
                        img,
                        (x1, label_y1),
                        (min(w - 1, x1 + text_w + 14), label_y2),
                        box_color,
                        cv2.FILLED,
                    )
                    cv2.putText(
                        img,
                        label,
                        (x1 + 6, max(14, y1 - 6)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        font_scale,
                        (255, 255, 255),
                        font_thickness,
                        cv2.LINE_AA,
                    )

                cv2.imwrite(str(output_file), img, [cv2.IMWRITE_JPEG_QUALITY, 95])

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