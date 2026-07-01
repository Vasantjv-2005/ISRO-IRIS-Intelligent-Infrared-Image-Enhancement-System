"""
Report Schemas

Request and response schemas for PDF report generation.
"""

from pydantic import BaseModel, Field

from app.schemas.detection_schema import DetectionObjectSchema


class ReportRequestSchema(BaseModel):
    """
    Request for generating a PDF report.
    """

    image_name: str = Field(
        ...,
        description="Original image filename.",
    )

    original_image_path: str = Field(
        ...,
        description="Path to the original uploaded image.",
    )

    processed_image_path: str = Field(
        ...,
        description="Path to the processed image.",
    )

    detected_objects: list[DetectionObjectSchema] = Field(
        default_factory=list,
        description="Detected objects.",
    )

    analysis: str = Field(
        ...,
        description="Gemini AI generated analysis.",
    )


class ReportResponseSchema(BaseModel):
    """
    Response after report generation.
    """

    success: bool = True

    report_path: str

    image_name: str

    generated_at: str

    total_detected_objects: int

    message: str = "Report generated successfully."