"""
Model Loader

Central registry for all AI models used by the
IRIS Backend.
"""

from __future__ import annotations

from app.ai_models.colorization_model import (
    ColorizationModel,
)
from app.ai_models.enhancement_model import (
    EnhancementModel,
)
from app.ai_models.gemini_client import (
    GeminiClient,
)
from app.ai_models.yolov8_model import (
    YOLOv8Model,
)


class ModelLoader:
    """
    Loads and manages all AI models.

    Models are loaded only once and reused
    throughout the application's lifetime.
    """

    def __init__(self) -> None:

        self._yolo: YOLOv8Model | None = None
        self._enhancement: EnhancementModel | None = None
        self._colorization: ColorizationModel | None = None
        self._gemini: GeminiClient | None = None

    # =====================================================
    # Load All Models
    # =====================================================

    def load_models(self) -> None:
        """
        Load every AI model.
        """

        self.get_yolo()

        self.get_enhancement()

        self.get_colorization()

        self.get_gemini()

    # =====================================================
    # YOLO
    # =====================================================

    def get_yolo(self) -> YOLOv8Model:
        """
        Return the YOLO model.
        """

        if self._yolo is None:

            self._yolo = YOLOv8Model()

            self._yolo.load()

        return self._yolo

    # =====================================================
    # Enhancement
    # =====================================================

    def get_enhancement(
        self,
    ) -> EnhancementModel:
        """
        Return the enhancement model.
        """

        if self._enhancement is None:

            self._enhancement = EnhancementModel()

            self._enhancement.load()

        return self._enhancement

    # =====================================================
    # Colorization
    # =====================================================

    def get_colorization(
        self,
    ) -> ColorizationModel:
        """
        Return the colorization model.
        """

        if self._colorization is None:

            self._colorization = ColorizationModel()

            self._colorization.load()

        return self._colorization

    # =====================================================
    # Gemini
    # =====================================================

    def get_gemini(
        self,
    ) -> GeminiClient:
        """
        Return the Gemini client.
        """

        if self._gemini is None:

            self._gemini = GeminiClient()

        return self._gemini

    # =====================================================
    # Model Information
    # =====================================================

    def info(self) -> dict:
        """
        Return information about loaded models.
        """

        return {
            "yolo_loaded": self._yolo is not None,
            "enhancement_loaded": self._enhancement is not None,
            "colorization_loaded": self._colorization is not None,
            "gemini_loaded": self._gemini is not None,
        }

    # =====================================================
    # Unload
    # =====================================================

    def unload(self) -> None:
        """
        Release all loaded models.
        """

        if self._yolo is not None:
            self._yolo.unload()

        self._yolo = None
        self._enhancement = None
        self._colorization = None
        self._gemini = None


# ==========================================================
# Singleton
# ==========================================================

model_loader = ModelLoader()