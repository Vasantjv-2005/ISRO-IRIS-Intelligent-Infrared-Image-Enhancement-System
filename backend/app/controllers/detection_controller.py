"""
Detection Controller

Handles object detection requests by delegating to DetectionService.
"""

from __future__ import annotations

from typing import Any

from app.services.ai.detection_service import detection_service


class DetectionController:
    """
    Controller responsible for object detection.
    """

    async def detect(
        self,
        image_path: str,
        output_directory: str,
        confidence: float = 0.25,
    ) -> dict[str, Any]:
        """
        Detect objects in an image.
        """
        return detection_service.detect(
            image_path=image_path,
            output_directory=output_directory,
            confidence=confidence,
        )


detection_controller = DetectionController()
