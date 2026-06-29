"""
Global Exception Handler

Registers all application exception handlers.
"""

from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.middleware.error_handler import IRISException


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all global exception handlers.
    """

    @app.exception_handler(IRISException)
    async def iris_exception_handler(
        request: Request,
        exc: IRISException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.message,
                "error": exc.error_code,
                "path": request.url.path,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "message": "Validation failed.",
                "error": "VALIDATION_ERROR",
                "details": exc.errors(),
                "path": request.url.path,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": str(exc.detail),
                "error": "HTTP_EXCEPTION",
                "path": request.url.path,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "An unexpected error occurred.",
                "error": "INTERNAL_SERVER_ERROR",
                "details": str(exc) if app.debug else None,
                "path": request.url.path,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )