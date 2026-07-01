"""
Response Utilities

Standardized API response helpers for the
IRIS Backend.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any


class ResponseBuilder:
    """
    Helper class for creating consistent
    API responses.
    """

    @staticmethod
    def success(
        message: str = "Success.",
        data: Any = None,
        status_code: int = 200,
    ) -> dict:
        """
        Build a successful response.
        """

        return {
            "success": True,
            "status_code": status_code,
            "message": message,
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
        }

    @staticmethod
    def created(
        message: str = "Resource created successfully.",
        data: Any = None,
    ) -> dict:
        """
        Build a 201 Created response.
        """

        return ResponseBuilder.success(
            message=message,
            data=data,
            status_code=201,
        )

    @staticmethod
    def updated(
        message: str = "Resource updated successfully.",
        data: Any = None,
    ) -> dict:
        """
        Build an update response.
        """

        return ResponseBuilder.success(
            message=message,
            data=data,
            status_code=200,
        )

    @staticmethod
    def deleted(
        message: str = "Resource deleted successfully.",
    ) -> dict:
        """
        Build a delete response.
        """

        return ResponseBuilder.success(
            message=message,
            status_code=200,
        )

    @staticmethod
    def error(
        message: str = "An error occurred.",
        error: Any = None,
        status_code: int = 500,
    ) -> dict:
        """
        Build an error response.
        """

        return {
            "success": False,
            "status_code": status_code,
            "message": message,
            "error": error,
            "timestamp": datetime.utcnow().isoformat(),
        }

    @staticmethod
    def paginated(
        *,
        items: list[Any],
        total: int,
        page: int,
        page_size: int,
        message: str = "Data retrieved successfully.",
    ) -> dict:
        """
        Build a paginated response.
        """

        total_pages = (
            (total + page_size - 1) // page_size
            if page_size > 0
            else 0
        )

        return {
            "success": True,
            "status_code": 200,
            "message": message,
            "data": items,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_items": total,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_previous": page > 1,
            },
            "timestamp": datetime.utcnow().isoformat(),
        }


response_builder = ResponseBuilder()