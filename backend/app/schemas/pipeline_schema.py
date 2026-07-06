"""
Pipeline Schemas
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class PipelineRequestSchema(BaseModel):
    """
    Inference pipeline request schema.
    """

    image_path: str = Field(
        ...,
        description="Path to the input infrared image.",
    )

    output_directory: str = Field(
        default="outputs",
        description="Directory where pipeline output files will be saved.",
    )

    confidence: float = Field(
        default=0.25,
        ge=0.0,
        le=1.0,
        description="Confidence threshold for YOLOv8 object detection.",
    )

    color_map: str | int = Field(
        default="inferno",
        description="Colormap for thermal colorization.",
    )


class PipelineResponseSchema(BaseModel):
    """
    Inference pipeline response schema.
    """

    success: bool
    upload_id: str
    processed_image: str
    preprocessed_image: str | None = None
    enhanced_image: str
    colorized_image: str
    detected_image: str | None = None
    analyzed_image: str | None = None
    detection_count: int
    analysis: str
    report_path: str
    message: str
