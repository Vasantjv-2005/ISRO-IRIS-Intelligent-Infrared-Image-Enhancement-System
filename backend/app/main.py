"""
Main application entry point for the IRIS Backend.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import (
    PROJECT_DESCRIPTION,
    PROJECT_NAME,
    PROJECT_VERSION,
)
from app.core.router import api_router
from app.core.settings import settings
from app.database.indexes import create_indexes
from app.database.mongodb import mongodb
from app.middleware.exception_handler import register_exception_handlers
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle manager.
    """

    # ---------------------------------------
    # Startup
    # ---------------------------------------
    logger.info("Initializing IRIS Backend services (v%s)...", PROJECT_VERSION)
    try:
        logger.info("Connecting to MongoDB Atlas...")
        await mongodb.connect()

        logger.info("Creating MongoDB indexes...")
        await create_indexes()

        logger.info("🚀 IRIS Backend Started Successfully")
        print("🚀 IRIS Backend Started Successfully")
    except Exception as exc:
        logger.warning("⚠️ MongoDB Atlas connection timed out or unavailable during startup: %s. Continuing startup.", exc)
        print(f"⚠️ MongoDB Startup Notice: {exc} (Backend operating resiliently)")

    yield

    # ---------------------------------------
    # Shutdown
    # ---------------------------------------
    logger.info("Shutting down IRIS Backend services...")
    try:
        await mongodb.disconnect()
        logger.info("🛑 IRIS Backend Stopped Cleanly")
        print("🛑 IRIS Backend Stopped")
    except Exception as exc:
        logger.error("❌ Error during MongoDB disconnection: %s", exc, exc_info=True)


app = FastAPI(
    title=PROJECT_NAME,
    description=PROJECT_DESCRIPTION,
    version=PROJECT_VERSION,
    lifespan=lifespan,
)

# Register exception handlers
register_exception_handlers(app)

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_origin_regex="http://(localhost|127\\.0\\.0\\.1)(:[0-9]+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/",
    tags=["Home"],
)
async def home():
    """
    Home endpoint.
    """

    return {
        "success": True,
        "message": "Welcome to IRIS Backend 🚀",
        "project": PROJECT_NAME,
        "version": PROJECT_VERSION,
    }


# ---------------------------------------
# Register API Routes
# ---------------------------------------

app.include_router(api_router)