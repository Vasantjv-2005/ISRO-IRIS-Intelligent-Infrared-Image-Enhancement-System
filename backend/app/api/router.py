"""
Central API Router for the IRIS Backend.

This module creates the main API router. Individual route
modules (upload, preprocessing, detection, etc.) will be
registered here as they are implemented.
"""

from fastapi import APIRouter

router = APIRouter(
    prefix="/api",
    tags=["IRIS API"],
)