"""
Main application entry point for the IRIS Backend.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import router
from app.core.config import (
    PROJECT_DESCRIPTION,
    PROJECT_NAME,
    PROJECT_VERSION,
)
from app.database.indexes import create_indexes
from app.database.mongodb import mongodb


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown events.
    """

    # ==========================
    # Startup
    # ==========================

    await mongodb.connect()

    await create_indexes()

    print("🚀 IRIS Backend Started Successfully")

    yield

    # ==========================
    # Shutdown
    # ==========================

    await mongodb.disconnect()

    print("🛑 IRIS Backend Stopped")


app = FastAPI(
    title=PROJECT_NAME,
    description=PROJECT_DESCRIPTION,
    version=PROJECT_VERSION,
    lifespan=lifespan,
)


@app.get("/", tags=["Home"])
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


app.include_router(router)