"""
AI Analysis Service

Uses Google Gemini to analyze infrared images and detected objects,
integrating with the repository layer for persistence.
"""

from __future__ import annotations

from typing import Any

import google.generativeai as genai

from app.core.settings import settings
from app.middleware.error_handler import AIModelException
from app.models.analysis_model import (
    AnalysisModel,
    AnalysisStatus,
    DetectedObject,
    utc_now,
)
from app.repositories.analysis_repository import analysis_repository
from app.repositories.upload_repository import upload_repository
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


class AnalysisService:
    """
    Service responsible for scene analysis using Gemini.
    """

    def __init__(self) -> None:
        """
        Initialize the AnalysisService and configure Gemini.
        """
        self.model: Any = None
        self._initialize()

    def _initialize(self) -> None:
        """
        Initialize the Gemini model SDK.
        """
        try:
            if settings.GEMINI_API_KEY:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.model = genai.GenerativeModel("gemini-2.5-flash")
                logger.info("Gemini GenerativeModel successfully initialized.")
            else:
                logger.warning("GEMINI_API_KEY is not set. Relying on Groq fallback.")
        except Exception as exc:
            logger.warning("Failed to initialize Gemini SDK (%s). Relying on Groq fallback.", exc)

    def analyze(
        self,
        detected_objects: list[dict[str, Any]],
        image_name: str,
    ) -> dict[str, Any]:
        """
        Analyze detected objects using Gemini with automatic fallback to Groq AI.

        Args:
            detected_objects: Objects detected by YOLO.
            image_name: Image filename.

        Returns:
            Dictionary containing AI analysis results.
        """
        try:
            logger.info("Starting AI scene analysis for image: %s", image_name)

            if not detected_objects:
                prompt = f"""
                Analyze an infrared image named '{image_name}'.

                No objects were detected.

                Explain what could be present,
                possible environmental conditions,
                and limitations.
                """
            else:
                object_names = ", ".join(
                    str(item.get("class_name", "unknown"))
                    for item in detected_objects
                )

                prompt = f"""
                Analyze the infrared image '{image_name}'.

                Detected objects:
                {object_names}

                Provide:
                1. Scene summary
                2. Important observations
                3. Potential risks
                4. Recommended actions
                5. Confidence in interpretation
                """

            analysis_text = ""
            if self.model and settings.GEMINI_API_KEY:
                try:
                    response = self.model.generate_content(prompt)
                    analysis_text = getattr(response, "text", str(response)).strip()
                    logger.info("Successfully completed Gemini scene analysis for: %s", image_name)
                except Exception as gemini_err:
                    logger.warning("Gemini analysis failed (%s). Attempting fallback to Groq AI...", gemini_err)

            if not analysis_text and settings.GROQ_API_KEY:
                try:
                    from groq import Groq
                    groq_client = Groq(api_key=settings.GROQ_API_KEY)
                    completion = groq_client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model=settings.GROQ_MODEL or "llama-3.3-70b-versatile",
                    )
                    if completion.choices and completion.choices[0].message.content:
                        analysis_text = completion.choices[0].message.content.strip()
                        logger.info("Successfully completed Groq AI scene analysis for: %s", image_name)
                except Exception as groq_err:
                    logger.error("Groq AI analysis failed for %s: %s", image_name, groq_err, exc_info=True)
                    raise AIModelException(f"Both Gemini and Groq analysis failed. Groq error: {groq_err}") from groq_err

            if not analysis_text:
                raise AIModelException("AI analysis failed: Neither Gemini nor Groq produced valid output or API keys are missing.")

            return {
                "success": True,
                "image": image_name,
                "analysis": analysis_text,
            }

        except Exception as exc:
            logger.error("AI scene analysis failed for %s: %s", image_name, exc, exc_info=True)
            if isinstance(exc, AIModelException):
                raise
            raise AIModelException(f"AI analysis failed: {exc}") from exc

    async def analyze_async(
        self,
        detected_objects: list[dict[str, Any]],
        image_name: str,
        upload_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Execute analysis and persist the results in the database repositories.

        Args:
            detected_objects: Objects detected by YOLO.
            image_name: Image filename.
            upload_id: Optional upload identifier for repository persistence.

        Returns:
            Dictionary containing AI analysis results.
        """
        result = self.analyze(detected_objects=detected_objects, image_name=image_name)

        if upload_id:
            try:
                converted_objects = [
                    DetectedObject(
                        label=str(obj.get("class_name", "unknown")),
                        confidence=float(obj.get("confidence", 0.0)),
                        bounding_box=list(obj.get("bbox", [])),
                    )
                    for obj in detected_objects
                ]

                analysis_doc = AnalysisModel(
                    upload_id=upload_id,
                    image_name=image_name,
                    status=AnalysisStatus.COMPLETED,
                    scene_summary=result["analysis"][:200] + "..." if len(result["analysis"]) > 200 else result["analysis"],
                    detailed_analysis=result["analysis"],
                    detected_objects=converted_objects,
                    object_count=len(converted_objects),
                    confidence_score=0.85 if converted_objects else 0.50,
                    analyzed_at=utc_now(),
                )

                await analysis_repository.create(analysis_doc)
                await upload_repository.save_analysis(
                    upload_id=upload_id,
                    objects_detected=detected_objects,
                    scene_summary=analysis_doc.scene_summary or "",
                )
                logger.info("Persisted analysis results to database for upload: %s", upload_id)
            except Exception as exc:
                logger.warning("Failed to persist analysis to DB for upload %s: %s", upload_id, exc)

        return result


analysis_service = AnalysisService()