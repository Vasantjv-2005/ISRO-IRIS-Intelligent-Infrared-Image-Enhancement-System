"""
Upload Repository

Handles all database operations related to uploaded images.
"""

from __future__ import annotations

from datetime import datetime
from typing import List

from pymongo import ReturnDocument

from app.database.mongodb import get_database
from app.models.upload_model import (
    ProcessingStatus,
    UploadModel,
    utc_now,
)
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


class UploadRepository:
    """
    Repository responsible for Upload collection.
    """

    COLLECTION = "uploads"

    @property
    def collection(self):
        """
        Return MongoDB uploads collection.
        """

        db = get_database()

        return db[self.COLLECTION]

    # =====================================================
    # Create
    # =====================================================

    async def create(
        self,
        upload: UploadModel,
    ) -> UploadModel:
        """
        Insert a new upload document.
        """

        document = upload.model_dump()

        await self.collection.insert_one(document)

        logger.info(
            "Upload created: %s",
            upload.filename,
        )

        return upload

    # =====================================================
    # Find by Upload ID
    # =====================================================

    async def get_by_upload_id(
        self,
        upload_id: str,
    ) -> UploadModel | None:
        """
        Find upload by upload_id.
        """

        document = await self.collection.find_one(
            {
                "upload_id": upload_id
            }
        )

        if document is None:
            return None

        document.pop("_id", None)

        return UploadModel(**document)

    # =====================================================
    # Find by Filename
    # =====================================================

    async def get_by_filename(
        self,
        filename: str,
    ) -> UploadModel | None:
        """
        Find upload by filename.
        """

        document = await self.collection.find_one(
            {
                "filename": filename
            }
        )

        if document is None:
            return None

        document.pop("_id", None)

        return UploadModel(**document)

    # =====================================================
    # Update Status
    # =====================================================

    async def update_status(
        self,
        upload_id: str,
        status: ProcessingStatus,
    ) -> bool:
        """
        Update processing status.
        """

        result = await self.collection.update_one(
            {
                "upload_id": upload_id
            },
            {
                "$set": {
                    "status": status,
                    "updated_at": utc_now(),
                }
            },
        )

        return result.modified_count > 0

    # =====================================================
    # Update Flags
    # =====================================================

    async def update_processing_flags(
        self,
        upload_id: str,
        *,
        preprocessing: bool | None = None,
        enhancement: bool | None = None,
        colorization: bool | None = None,
        detection: bool | None = None,
        analysis: bool | None = None,
        report: bool | None = None,
    ) -> bool:
        """
        Update processing completion flags.
        """

        updates = {
            "updated_at": utc_now(),
        }

        if preprocessing is not None:
            updates["preprocessing_completed"] = preprocessing

        if enhancement is not None:
            updates["enhancement_completed"] = enhancement

        if colorization is not None:
            updates["colorization_completed"] = colorization

        if detection is not None:
            updates["detection_completed"] = detection

        if analysis is not None:
            updates["analysis_completed"] = analysis

        if report is not None:
            updates["report_generated"] = report

        result = await self.collection.update_one(
            {
                "upload_id": upload_id
            },
            {
                "$set": updates
            },
        )

        return result.modified_count > 0

    # =====================================================
    # Save Preprocessing Path
    # =====================================================

    async def save_preprocessing_path(
        self,
        upload_id: str,
        preprocessed_path: str,
    ) -> bool:
        """
        Save preprocessed image path and flag.
        """

        result = await self.collection.update_one(
            {
                "upload_id": upload_id
            },
            {
                "$set": {
                    "preprocessed_path": preprocessed_path,
                    "preprocessing_completed": True,
                    "updated_at": utc_now(),
                }
            },
        )

        return result.modified_count > 0

    # =====================================================
    # Save Enhancement Path
    # =====================================================

    async def save_enhancement_path(
        self,
        upload_id: str,
        enhanced_path: str,
    ) -> bool:
        """
        Save enhanced image path and flag.
        """

        result = await self.collection.update_one(
            {
                "upload_id": upload_id
            },
            {
                "$set": {
                    "enhanced_path": enhanced_path,
                    "enhancement_completed": True,
                    "updated_at": utc_now(),
                }
            },
        )

        return result.modified_count > 0

    # =====================================================
    # Save Colorization Path
    # =====================================================

    async def save_colorization_path(
        self,
        upload_id: str,
        colorized_path: str,
    ) -> bool:
        """
        Save colorized image path and flag.
        """

        result = await self.collection.update_one(
            {
                "upload_id": upload_id
            },
            {
                "$set": {
                    "colorized_path": colorized_path,
                    "colorization_completed": True,
                    "updated_at": utc_now(),
                }
            },
        )

        return result.modified_count > 0

    # =====================================================
    # Save Detection Results
    # =====================================================

    async def save_detection_results(
        self,
        upload_id: str,
        objects_detected: list,
        detected_path: str | None = None,
    ) -> bool:
        """
        Save object detection results and optional image path.
        """

        set_fields: dict = {
            "objects_detected": objects_detected,
            "detection_completed": True,
            "updated_at": utc_now(),
        }
        if detected_path:
            set_fields["detected_path"] = detected_path

        result = await self.collection.update_one(
            {
                "upload_id": upload_id
            },
            {
                "$set": set_fields
            },
        )

        return result.modified_count > 0

    # =====================================================
    # Save Analysis
    # =====================================================

    async def save_analysis(
        self,
        upload_id: str,
        objects_detected: list,
        scene_summary: str,
        analyzed_path: str | None = None,
    ) -> bool:
        """
        Save AI analysis.
        """

        set_fields: dict = {
            "objects_detected": objects_detected,
            "scene_summary": scene_summary,
            "analysis_completed": True,
            "updated_at": utc_now(),
        }
        if analyzed_path:
            set_fields["analyzed_path"] = analyzed_path

        result = await self.collection.update_one(
            {
                "upload_id": upload_id
            },
            {
                "$set": set_fields
            },
        )

        return result.modified_count > 0

    # =====================================================
    # Save Report
    # =====================================================

    async def save_report_path(
        self,
        upload_id: str,
        report_path: str,
    ) -> bool:
        """
        Save generated report path.
        """

        result = await self.collection.update_one(
            {
                "upload_id": upload_id
            },
            {
                "$set": {
                    "report_path": report_path,
                    "report_generated": True,
                    "updated_at": utc_now(),
                }
            },
        )

        return result.modified_count > 0

    # =====================================================
    # Mark As Failed
    # =====================================================

    async def mark_as_failed(
        self,
        upload_id: str,
        error_message: str,
    ) -> bool:
        """
        Mark upload as failed.
        """

        result = await self.collection.update_one(
            {
                "upload_id": upload_id
            },
            {
                "$set": {
                    "status": ProcessingStatus.FAILED,
                    "updated_at": utc_now(),
                }
            },
        )

        return result.modified_count > 0

    # =====================================================
    # Delete
    # =====================================================

    async def delete(
        self,
        upload_id: str,
    ) -> bool:
        """
        Delete upload.
        """

        result = await self.collection.delete_one(
            {
                "upload_id": upload_id
            }
        )

        return result.deleted_count > 0

    # =====================================================
    # List Uploads
    # =====================================================

    async def list_uploads(
        self,
        limit: int = 100,
    ) -> List[UploadModel]:
        """
        Return latest uploads.
        """

        cursor = (
            self.collection
            .find()
            .sort(
                "uploaded_at",
                -1,
            )
            .limit(limit)
        )

        uploads: List[UploadModel] = []

        async for document in cursor:

            document.pop("_id", None)

            uploads.append(
                UploadModel(**document)
            )

        return uploads

    # =====================================================
    # Count
    # =====================================================

    async def count(self) -> int:
        """
        Return total uploads.
        """

        return await self.collection.count_documents({})

    # =====================================================
    # Exists
    # =====================================================

    async def exists(
        self,
        upload_id: str,
    ) -> bool:
        """
        Check if upload exists.
        """

        count = await self.collection.count_documents(
            {
                "upload_id": upload_id
            },
            limit=1,
        )

        return count > 0

    # =====================================================
    # Dashboard Statistics & Aggregations
    # =====================================================

    async def get_upload_statistics(self) -> dict:
        """
        Compute dashboard upload metrics.
        """

        total_uploads = await self.count()
        total_processed = await self.collection.count_documents({"status": "completed"})
        total_reports = await self.collection.count_documents({"report_generated": True})
        total_completed_analysis = await self.collection.count_documents({"analysis_completed": True})
        total_failed_jobs = await self.collection.count_documents({"status": "failed"})

        pipeline_objects = [
            {"$project": {"count": {"$size": {"$ifNull": ["$objects_detected", []]}}}},
            {"$group": {"_id": None, "total": {"$sum": "$count"}}},
        ]
        cursor_objects = self.collection.aggregate(pipeline_objects)
        res_objects = await cursor_objects.to_list(1)
        total_objects = res_objects[0]["total"] if res_objects else 0

        pipeline_storage = [
            {"$group": {"_id": None, "total_size": {"$sum": "$file_size"}}}
        ]
        cursor_storage = self.collection.aggregate(pipeline_storage)
        res_storage = await cursor_storage.to_list(1)
        total_size_bytes = res_storage[0]["total_size"] if res_storage else 0

        return {
            "total_uploads": total_uploads,
            "total_processed_images": total_processed,
            "total_reports_generated": total_reports,
            "total_completed_analysis": total_completed_analysis,
            "total_failed_jobs": total_failed_jobs,
            "total_objects_detected": total_objects,
            "total_size_bytes": total_size_bytes,
        }

    async def get_recent_uploads(
        self,
        limit: int = 5,
    ) -> list[dict]:
        """
        Return recent upload activities for the dashboard.
        """

        cursor = self.collection.find().sort("uploaded_at", -1).limit(limit)
        recent = []
        async for doc in cursor:
            recent.append({
                "upload_id": str(doc.get("upload_id") or doc.get("_id") or ""),
                "filename": doc.get("filename", ""),
                "status": doc.get("status", "uploaded"),
                "uploaded_at": doc.get("uploaded_at") or doc.get("created_at") or utc_now(),
            })
        return recent


upload_repository = UploadRepository()