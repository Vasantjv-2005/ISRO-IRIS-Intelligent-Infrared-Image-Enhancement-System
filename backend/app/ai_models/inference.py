"""
Inference Engine

Runs the complete AI inference pipeline.

Pipeline:

Input Image
      │
      ▼
Enhancement
      │
      ▼
Colorization
      │
      ▼
YOLO Detection
      │
      ▼
Gemini Analysis
      │
      ▼
Return Result
"""

from __future__ import annotations

from pathlib import Path

from app.ai_models.model_loader import model_loader


class InferenceEngine:
    """
    Executes the complete AI inference pipeline.
    """

    def __init__(self) -> None:

        self.enhancement_model = (
            model_loader.get_enhancement()
        )

        self.colorization_model = (
            model_loader.get_colorization()
        )

        self.yolo_model = (
            model_loader.get_yolo()
        )

        self.gemini_client = (
            model_loader.get_gemini()
        )

    # =====================================================
    # Run Complete Pipeline
    # =====================================================

    def run(
        self,
        image_path: str,
        output_directory: str = "outputs",
        confidence: float = 0.25,
    ) -> dict:
        """
        Execute the complete AI pipeline.
        """

        image = Path(image_path)

        if not image.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        output_dir = Path(output_directory)

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        # -------------------------------------------------
        # Output folders
        # -------------------------------------------------

        enhancement_dir = (
            output_dir / "enhancement"
        )

        colorization_dir = (
            output_dir / "colorization"
        )

        detection_dir = (
            output_dir / "detection"
        )

        enhancement_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        colorization_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        detection_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        # -------------------------------------------------
        # File Names
        # -------------------------------------------------

        enhanced_image = (
            enhancement_dir / image.name
        )

        colorized_image = (
            colorization_dir / image.name
        )

        # -------------------------------------------------
        # Enhancement
        # -------------------------------------------------

        enhanced_path = (
            self.enhancement_model.enhance(
                input_path=str(image),
                output_path=str(enhanced_image),
            )
        )

        # -------------------------------------------------
        # Colorization
        # -------------------------------------------------

        colorized_path = (
            self.colorization_model.colorize(
                input_path=enhanced_path,
                output_path=str(colorized_image),
            )
        )

        # -------------------------------------------------
        # Detection
        # -------------------------------------------------

        detections = (
            self.yolo_model.predict(
                image_path=colorized_path,
                confidence=confidence,
                save=True,
                output_directory=str(
                    detection_dir
                ),
            )
        )

        # -------------------------------------------------
        # Gemini Analysis
        # -------------------------------------------------

        analysis = (
            self.gemini_client.analyze_scene(
                image_name=image.name,
                detected_objects=detections,
            )
        )

        # -------------------------------------------------
        # Response
        # -------------------------------------------------

        return {
            "success": True,
            "original_image": str(image),
            "enhanced_image": enhanced_path,
            "colorized_image": colorized_path,
            "detections": detections,
            "analysis": analysis,
            "total_objects": len(
                detections
            ),
        }


# ==========================================================
# Singleton
# ==========================================================

inference_engine = InferenceEngine()