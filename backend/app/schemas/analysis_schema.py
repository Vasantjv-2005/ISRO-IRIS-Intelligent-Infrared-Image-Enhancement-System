"""
Analysis Schemas

Request and response schemas for AI scene analysis.
"""

from pydantic import BaseModel, Field

from app.schemas.detection_schema import DetectionObjectSchema


class AnalysisRequestSchema(BaseModel):
    """
    AI analysis request.
    """

    image_name: str = Field(
        ...,
        description="Image filename.",
    )

    detected_objects: list[DetectionObjectSchema] = Field(
        default_factory=list,
        description="Objects detected by YOLO.",
    )


class AnalysisResponseSchema(BaseModel):
    """
    AI analysis response.
    """

    success: bool = True

    image: str

    analysis: str

    model: str = "Gemini"

    total_detected_objects: int

    message: str = "Scene analysis completed successfully."