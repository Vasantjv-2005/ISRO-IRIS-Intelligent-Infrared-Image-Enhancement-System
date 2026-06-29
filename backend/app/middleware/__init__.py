"""
Middleware Package

Exports all middleware setup functions and custom exceptions
used by the IRIS Backend.
"""

from app.middleware.cors import setup_cors
from app.middleware.error_handler import (
    AIModelException,
    BadRequestException,
    ConflictException,
    DatabaseException,
    ExternalServiceException,
    FileUploadException,
    ForbiddenException,
    ImageProcessingException,
    IRISException,
    NotFoundException,
    ReportGenerationException,
    UnauthorizedException,
    ValidationException,
)
from app.middleware.exception_handler import register_exception_handlers
from app.middleware.request_logger import setup_request_logger

__all__ = [
    "setup_cors",
    "setup_request_logger",
    "register_exception_handlers",
    "IRISException",
    "BadRequestException",
    "UnauthorizedException",
    "ForbiddenException",
    "NotFoundException",
    "ConflictException",
    "ValidationException",
    "FileUploadException",
    "ImageProcessingException",
    "AIModelException",
    "DatabaseException",
    "ReportGenerationException",
    "ExternalServiceException",
]