"""
Detection Schemas

Request and response schemas for object detection.
"""

from pydantic import BaseModel, Field


class DetectionRequestSchema(BaseModel):
    """
    Object detection request.
    """

    image_path: str = Field(
        ...,
        description="Path to the input image.",
    )

    output_directory: str = Field(
        default="outputs/detections",
        description="Directory where detection results will be stored.",
    )

    confidence: float = Field(
        default=0.25,
        ge=0.0,
        le=1.0,
        description="Minimum confidence threshold.",
    )


class BoundingBoxSchema(BaseModel):
    """
    Bounding box coordinates.
    """

    x1: float
    y1: float
    x2: float
    y2: float


class DetectionObjectSchema(BaseModel):
    """
    Single detected object.
    """

    class_id: int

    class_name: str

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
    )

    bbox: BoundingBoxSchema


class DetectionResponseSchema(BaseModel):
    """
    Detection response.
    """

    success: bool

    image_path: str

    output_directory: str

    total_objects: int

    detections: list[DetectionObjectSchema]

    message: str = "Object detection completed successfully."