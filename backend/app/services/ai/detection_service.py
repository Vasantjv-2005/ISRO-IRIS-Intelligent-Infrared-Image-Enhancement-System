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
                font_scale = max(0.48, min(0.65, max(h, w) / 2000.0))
                font_thickness = 1
                line_thick = 2

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

                # 1. First pass: Draw all bounding box rectangles cleanly underneath
                for det in detections:
                    bbox = det.get("bbox", {})
                    x1 = max(0, int(bbox.get("x1", 0)))
                    y1 = max(0, int(bbox.get("y1", 0)))
                    x2 = min(w - 1, int(bbox.get("x2", 0)))
                    y2 = min(h - 1, int(bbox.get("y2", 0)))

                    cname = det.get("class_name", "OBJECT")
                    box_color = color_palette.get(cname.upper(), (255, 160, 40))
                    cv2.rectangle(img, (x1, y1), (x2, y2), box_color, line_thick, cv2.LINE_AA)

                # 2. Second pass: Structured label placement with zero overlap and clean stacking
                placed_banners = []

                def check_banner_overlap(r1, r2, pad=3):
                    return not (r1[2] + pad <= r2[0] or r1[0] >= r2[2] + pad or
                                r1[3] + pad <= r2[1] or r1[1] >= r2[3] + pad)

                for det in detections:
                    bbox = det.get("bbox", {})
                    x1 = max(0, int(bbox.get("x1", 0)))
                    y1 = max(0, int(bbox.get("y1", 0)))
                    x2 = min(w - 1, int(bbox.get("x2", 0)))
                    y2 = min(h - 1, int(bbox.get("y2", 0)))

                    cname = det.get("class_name", "OBJECT")
                    box_color = color_palette.get(cname.upper(), (255, 160, 40))

                    conf_val = float(det.get("confidence", 0.0))
                    conf_pct = round(conf_val * 100.0)
                    label = f"{cname} {conf_pct}%"
                    (text_w, text_h), baseline = cv2.getTextSize(
                        label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness
                    )
                    banner_w = text_w + 10
                    banner_h = text_h + baseline + 8

                    # Generate structured candidate locations around the bounding box
                    candidates = [
                        (x1, y1 - banner_h - 2),                          # 1. Above top-left
                        (x1, y1 + 2),                                     # 2. Inside top-left
                        (x1, y2 + 2),                                     # 3. Below bottom-left
                        (max(0, x2 - banner_w), y1 - banner_h - 2),       # 4. Above top-right
                        (max(0, x2 - banner_w), y1 + 2),                  # 5. Inside top-right
                        (max(0, x2 - banner_w), y2 + 2),                  # 6. Below bottom-right
                        (x1, max(0, int((y1 + y2 - banner_h) / 2))),      # 7. Middle left
                    ]
                    # Multi-tiered vertical stacking for dense/overlapping detections
                    for step in range(1, 10):
                        candidates.append((x1, y1 - banner_h - 2 - step * (banner_h + 3)))             # Stack above top-left
                        candidates.append((x1, y2 + 2 + step * (banner_h + 3)))                        # Stack below bottom-left
                        candidates.append((x1, y1 + 2 + step * (banner_h + 3)))                        # Stack inside downwards
                        candidates.append((max(0, x2 - banner_w), y1 - banner_h - 2 - step * (banner_h + 3))) # Stack above top-right
                        candidates.append((max(0, x2 - banner_w), y2 + 2 + step * (banner_h + 3)))            # Stack below bottom-right

                    best_rect = None
                    for cand_x, cand_y in candidates:
                        cx = max(0, min(w - banner_w, cand_x))
                        cy = max(0, min(h - banner_h, cand_y))
                        rect = (cx, cy, cx + banner_w, cy + banner_h)
                        if not any(check_banner_overlap(rect, pb) for pb in placed_banners):
                            best_rect = rect
                            break

                    # Fallback scan if all structured candidates overlap in extremely dense regions
                    if best_rect is None:
                        found_fallback = False
                        for scan_y in range(max(0, y1 - banner_h - 2), h - banner_h, banner_h + 2):
                            rect = (max(0, min(w - banner_w, x1)), scan_y, max(0, min(w - banner_w, x1)) + banner_w, scan_y + banner_h)
                            if not any(check_banner_overlap(rect, pb) for pb in placed_banners):
                                best_rect = rect
                                found_fallback = True
                                break
                        if not found_fallback:
                            best_rect = (max(0, min(w - banner_w, x1)), max(0, min(h - banner_h, y1 - banner_h - 2)), max(0, min(w - banner_w, x1)) + banner_w, max(0, min(h - banner_h, y1 - banner_h - 2)) + banner_h)

                    bx1, by1, bx2, by2 = best_rect
                    placed_banners.append(best_rect)

                    cv2.rectangle(img, (bx1, by1), (bx2, by2), box_color, cv2.FILLED)
                    cv2.putText(
                        img,
                        label,
                        (bx1 + 5, by2 - baseline - 4),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        font_scale,
                        (255, 255, 255),
                        font_thickness,
                        cv2.LINE_AA,
                    )

                cv2.imwrite(str(output_file), img, [cv2.IMWRITE_JPEG_QUALITY, 100])

            # Compute summary table detailing total pixel counts, area coverage %, and object counts
            total_img_pixels = max(1, h * w)
            summary_map: dict[str, dict[str, Any]] = {}
            for det in detections:
                c_name = str(det.get("class_name", "UNKNOWN")).upper()
                bx = det.get("bbox", {})
                w_px = max(0, bx.get("x2", 0) - bx.get("x1", 0))
                h_px = max(0, bx.get("y2", 0) - bx.get("y1", 0))
                box_pixels = w_px * h_px
                if c_name not in summary_map:
                    summary_map[c_name] = {"class_name": c_name, "object_count": 0, "pixel_count": 0, "area_coverage_pct": 0.0}
                summary_map[c_name]["object_count"] += 1
                summary_map[c_name]["pixel_count"] += box_pixels

            class_summary = []
            for c_name, data in summary_map.items():
                pct = round(min(100.0, (data["pixel_count"] / float(total_img_pixels)) * 100.0), 2)
                data["area_coverage_pct"] = pct
                class_summary.append(data)

            return {
                "success": True,
                "image_path": image_path,
                "output_directory": output_directory,
                "output_path": str(output_file),
                "detected_image_path": str(output_file),
                "total_objects": len(detections),
                "class_summary": class_summary,
                "detections": detections,
            }
        except Exception as exc:
            logger.error("Detection execution failed for %s: %s", image_path, exc, exc_info=True)
            raise ImageProcessingException(f"Detection execution failed: {exc}") from exc


detection_service = DetectionService()