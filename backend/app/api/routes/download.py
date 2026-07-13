"""
Download Routes

Provides endpoints for downloading generated images and reports.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from app.controllers.download_controller import download_controller

router = APIRouter(
    prefix="/download",
    tags=["Download"],
)


@router.get(
    "/",
    summary="Download a file",
)
async def download_file(
    file_path: str,
    inline: bool = False,
):
    """
    Download or view a file from the server.
    """
    try:
        file_info = download_controller.get_file(file_path)

        return FileResponse(
            path=file_info["path"],
            filename=file_info["filename"],
            media_type=file_info["mime_type"],
            content_disposition_type="inline" if inline else "attachment",
        )
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    except IsADirectoryError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while preparing download: {exc}",
        )
