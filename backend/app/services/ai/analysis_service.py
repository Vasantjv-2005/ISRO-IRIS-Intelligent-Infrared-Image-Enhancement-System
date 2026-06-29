"""
AI Analysis Service

Uses Google Gemini to analyze infrared images
and detected objects.
"""

from __future__ import annotations

from typing import Any

import google.generativeai as genai

from app.core.settings import settings
from app.middleware.error_handler import AIModelException


class AnalysisService:
    """
    Service responsible for scene analysis using Gemini.
    """

    def __init__(self) -> None:
        self.model = None
        self._initialize()

    def _initialize(self) -> None:
        """
        Initialize the Gemini model.
        """

        try:
            genai.configure(
                api_key=settings.GEMINI_API_KEY,
            )

            self.model = genai.GenerativeModel(
                "gemini-2.5-flash"
            )

        except Exception as exc:
            raise AIModelException(
                f"Failed to initialize Gemini: {exc}"
            )

    def analyze(
        self,
        detected_objects: list[dict[str, Any]],
        image_name: str,
    ) -> dict[str, Any]:
        """
        Analyze detected objects using Gemini.

        Args:
            detected_objects:
                Objects detected by YOLO.

            image_name:
                Image filename.

        Returns:
            AI analysis.
        """

        try:

            if not detected_objects:
                prompt = f"""
                Analyze an infrared image named
                '{image_name}'.

                No objects were detected.

                Explain what could be present,
                possible environmental conditions,
                and limitations.
                """

            else:

                object_names = ", ".join(
                    item["class_name"]
                    for item in detected_objects
                )

                prompt = f"""
                Analyze the infrared image
                '{image_name}'.

                Detected objects:

                {object_names}

                Provide:

                1. Scene summary
                2. Important observations
                3. Potential risks
                4. Recommended actions
                5. Confidence in interpretation
                """

            response = self.model.generate_content(
                prompt
            )

            return {
                "success": True,
                "image": image_name,
                "analysis": response.text,
            }

        except Exception as exc:
            raise AIModelException(
                f"Gemini analysis failed: {exc}"
            )


analysis_service = AnalysisService()