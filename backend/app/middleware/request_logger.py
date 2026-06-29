"""
Request Logger Middleware

Logs every incoming request and outgoing response.
"""

import logging
import time

from fastapi import FastAPI, Request


logger = logging.getLogger("iris.request")


def setup_request_logger(app: FastAPI) -> None:
    """
    Register request logging middleware.
    """

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.perf_counter()

        response = await call_next(request)

        process_time = time.perf_counter() - start_time

        logger.info(
            "%s | %s | %s | %s | %.4f sec",
            request.method,
            request.url.path,
            response.status_code,
            request.client.host if request.client else "Unknown",
            process_time,
        )

        response.headers["X-Process-Time"] = f"{process_time:.4f}"

        return response