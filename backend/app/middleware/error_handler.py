"""
Custom Error Classes

Defines reusable custom exceptions for the
IRIS Backend.
"""

from typing import Optional


class IRISException(Exception):
    """
    Base exception for the IRIS application.
    """

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "INTERNAL_SERVER_ERROR",
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

        super().__init__(message)


class BadRequestException(IRISException):
    """
    400 Bad Request
    """

    def __init__(self, message: str = "Bad request."):
        super().__init__(
            message=message,
            status_code=400,
            error_code="BAD_REQUEST",
        )


class UnauthorizedException(IRISException):
    """
    401 Unauthorized
    """

    def __init__(self, message: str = "Unauthorized access."):
        super().__init__(
            message=message,
            status_code=401,
            error_code="UNAUTHORIZED",
        )


class ForbiddenException(IRISException):
    """
    403 Forbidden
    """

    def __init__(self, message: str = "Access forbidden."):
        super().__init__(
            message=message,
            status_code=403,
            error_code="FORBIDDEN",
        )


class NotFoundException(IRISException):
    """
    404 Not Found
    """

    def __init__(self, message: str = "Resource not found."):
        super().__init__(
            message=message,
            status_code=404,
            error_code="NOT_FOUND",
        )


class ConflictException(IRISException):
    """
    409 Conflict
    """

    def __init__(self, message: str = "Resource already exists."):
        super().__init__(
            message=message,
            status_code=409,
            error_code="CONFLICT",
        )


class ValidationException(IRISException):
    """
    422 Validation Error
    """

    def __init__(self, message: str = "Validation failed."):
        super().__init__(
            message=message,
            status_code=422,
            error_code="VALIDATION_ERROR",
        )


class FileUploadException(IRISException):
    """
    Raised when image upload fails.
    """

    def __init__(self, message: str = "Image upload failed."):
        super().__init__(
            message=message,
            status_code=400,
            error_code="UPLOAD_ERROR",
        )


class ImageProcessingException(IRISException):
    """
    Raised when image preprocessing or enhancement fails.
    """

    def __init__(self, message: str = "Image processing failed."):
        super().__init__(
            message=message,
            status_code=500,
            error_code="IMAGE_PROCESSING_ERROR",
        )


class AIModelException(IRISException):
    """
    Raised when an AI model fails.
    """

    def __init__(self, message: str = "AI model execution failed."):
        super().__init__(
            message=message,
            status_code=500,
            error_code="AI_MODEL_ERROR",
        )


class DatabaseException(IRISException):
    """
    Raised for MongoDB-related errors.
    """

    def __init__(self, message: str = "Database operation failed."):
        super().__init__(
            message=message,
            status_code=500,
            error_code="DATABASE_ERROR",
        )


class ReportGenerationException(IRISException):
    """
    Raised when report generation fails.
    """

    def __init__(self, message: str = "Report generation failed."):
        super().__init__(
            message=message,
            status_code=500,
            error_code="REPORT_GENERATION_ERROR",
        )


class ExternalServiceException(IRISException):
    """
    Raised when an external service
    (Gemini, Hugging Face, etc.) fails.
    """

    def __init__(
        self,
        message: str = "External service unavailable.",
        service_name: Optional[str] = None,
    ):
        self.service_name = service_name

        super().__init__(
            message=message,
            status_code=503,
            error_code="EXTERNAL_SERVICE_ERROR",
        )


class WeightsException(AIModelException):
    """
    Base exception for all weight-related errors.
    """

    def __init__(self, message: str = "Weights error."):
        super().__init__(
            message=message,
        )
        self.error_code = "WEIGHTS_ERROR"


class WeightsNotFoundError(WeightsException):
    """
    Raised when weight files do not exist at the specified path.
    """

    def __init__(self, message: str = "Weight files not found."):
        super().__init__(
            message=message,
        )
        self.error_code = "WEIGHTS_NOT_FOUND"


class WeightsInvalidError(WeightsException):
    """
    Raised when weight files are present but invalid (e.g., empty placeholders).
    """

    def __init__(self, message: str = "Weight files are invalid."):
        super().__init__(
            message=message,
        )
        self.error_code = "WEIGHTS_INVALID"