"""
Analysis Controller

Handles AI scene analysis requests by delegating to the Analysis Service.
"""

from __future__ import annotations

from app.schemas.analysis_schema import (
    AnalysisRequestSchema,
    AnalysisResponseSchema,
)
from app.services.ai.analysis_service import analysis_service


class AnalysisController:
    """
    Controller responsible for AI scene analysis.
    """

    async def analyze_scene(
        self,
        request: AnalysisRequestSchema,
    ) -> AnalysisResponseSchema:
        """
        Analyze detected objects using Gemini AI.
        """

        result = analysis_service.analyze(
            detected_objects=[
                detection.model_dump()
                for detection in request.detected_objects
            ],
            image_name=request.image_name,
        )

        return AnalysisResponseSchema(
            success=True,
            image=result["image"],
            analysis=result["analysis"],
            model="Gemini",
            total_detected_objects=len(
                request.detected_objects
            ),
            message="Scene analysis completed successfully.",
        )


analysis_controller = AnalysisController()
