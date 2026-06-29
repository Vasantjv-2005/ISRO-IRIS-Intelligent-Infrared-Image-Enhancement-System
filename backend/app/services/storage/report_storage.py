"""
Report Storage Service

Handles storing and retrieving generated reports
from MongoDB.
"""

from datetime import datetime
from typing import Any

from bson import ObjectId

from app.database.mongodb import get_database


class ReportStorageService:
    """
    Service responsible for report storage.
    """

    def __init__(self):
        self.collection_name = "reports"

    async def save_report(
        self,
        report: dict[str, Any],
    ) -> str:
        """
        Save report metadata into MongoDB.

        Returns:
            Report ID
        """

        db = get_database()

        report["created_at"] = datetime.utcnow()
        report["updated_at"] = datetime.utcnow()

        result = await db[self.collection_name].insert_one(report)

        return str(result.inserted_id)

    async def get_report(
        self,
        report_id: str,
    ) -> dict[str, Any] | None:
        """
        Retrieve report by ID.
        """

        db = get_database()

        document = await db[self.collection_name].find_one(
            {
                "_id": ObjectId(report_id)
            }
        )

        if document:
            document["_id"] = str(document["_id"])

        return document

    async def update_report(
        self,
        report_id: str,
        updated_data: dict[str, Any],
    ) -> bool:
        """
        Update report metadata.
        """

        db = get_database()

        updated_data["updated_at"] = datetime.utcnow()

        result = await db[self.collection_name].update_one(
            {
                "_id": ObjectId(report_id)
            },
            {
                "$set": updated_data
            },
        )

        return result.modified_count > 0

    async def delete_report(
        self,
        report_id: str,
    ) -> bool:
        """
        Delete report.
        """

        db = get_database()

        result = await db[self.collection_name].delete_one(
            {
                "_id": ObjectId(report_id)
            }
        )

        return result.deleted_count > 0

    async def list_reports(
        self,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """
        Return recent reports.
        """

        db = get_database()

        cursor = (
            db[self.collection_name]
            .find()
            .sort("created_at", -1)
            .limit(limit)
        )

        reports = []

        async for report in cursor:
            report["_id"] = str(report["_id"])
            reports.append(report)

        return reports


report_storage = ReportStorageService()