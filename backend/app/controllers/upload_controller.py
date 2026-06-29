"""
Upload Controller

Handles upload-related requests by delegating
business logic to the Upload Service.
"""

from fastapi import UploadFile

from app.schemas.upload_schema import UploadResponseSchema
from app.services.upload.upload_service import upload_service


class UploadController:
    """
    Controller responsible for upload operations.
    """

    async def upload_image(
        self,
        file: UploadFile,
    ) -> UploadResponseSchema:
        """
        Upload an image.

        Args:
            file:
                Uploaded image.

        Returns:
            Upload response.
        """

        return await upload_service.upload_image(file)

    async def get_upload(
        self,
        upload_id: str,
    ):
        """
        Retrieve upload details.
        """

        return await upload_service.get_upload(
            upload_id
        )

    async def delete_upload(
        self,
        upload_id: str,
    ):
        """
        Delete an upload.
        """

        return await upload_service.delete_upload(
            upload_id
        )


upload_controller = UploadController()