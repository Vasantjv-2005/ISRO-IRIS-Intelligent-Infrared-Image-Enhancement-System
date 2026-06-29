"""
Common Response Schemas

Reusable API response schemas for the IRIS Backend.
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class ApiResponse(BaseModel):
    """
    Standard success response.
    """

    success: bool = True

    message: str

    data: Optional[Any] = None

    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    """
    Standard error response.
    """

    success: bool = False

    message: str

    error: Optional[str] = None

    details: Optional[Any] = None

    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PaginationResponse(BaseModel):
    """
    Pagination information.
    """

    page: int

    page_size: int

    total_records: int

    total_pages: int


class PaginatedResponse(ApiResponse):
    """
    Standard paginated API response.
    """

    pagination: PaginationResponse