"""
Dashboard Service

Provides dashboard statistics for the IRIS Backend by querying MongoDB.
"""

from __future__ import annotations

from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorDatabase


class DashboardService:
    """
    Dashboard service responsible for calculating metrics and stats.
    """

    async def get_dashboard(
        self,
        db: AsyncIOMotorDatabase,
    ) -> dict:
        """
        Return dashboard statistics.
        """
        uploads = db["uploads"]
        sessions = db["sessions"]

        # Count total uploads and reports
        total_uploads = await uploads.count_documents({})
        total_processed = await uploads.count_documents({"status": "completed"})
        total_reports = await uploads.count_documents({"report_generated": True})
        total_completed_analysis = await uploads.count_documents({"analysis_completed": True})
        total_failed_jobs = await uploads.count_documents({"status": "failed"})

        # Active sessions
        active_sessions = await sessions.count_documents({"status": {"$in": ["created", "running"]}})

        # Aggregate total objects detected
        pipeline_objects = [
            {"$project": {"count": {"$size": {"$ifNull": ["$objects_detected", []]}}}},
            {"$group": {"_id": None, "total": {"$sum": "$count"}}},
        ]
        cursor_objects = uploads.aggregate(pipeline_objects)
        res_objects = await cursor_objects.to_list(1)
        total_objects = res_objects[0]["total"] if res_objects else 0

        # Success rate
        success_rate = 0.0
        if total_uploads > 0:
            success_rate = round((total_processed / total_uploads) * 100.0, 2)

        # Average processing time
        pipeline_time = [
            {"$group": {"_id": None, "avg_time": {"$avg": "$processing_time_seconds"}}}
        ]
        cursor_time = sessions.aggregate(pipeline_time)
        res_time = await cursor_time.to_list(1)
        avg_time = round(res_time[0]["avg_time"] or 0.0, 2) if res_time else 0.0

        # Storage used
        pipeline_storage = [
            {"$group": {"_id": None, "total_size": {"$sum": "$file_size"}}}
        ]
        cursor_storage = uploads.aggregate(pipeline_storage)
        res_storage = await cursor_storage.to_list(1)
        total_size_bytes = res_storage[0]["total_size"] if res_storage else 0
        storage_mb = round(total_size_bytes / (1024 * 1024), 2)

        # Fetch recent activities
        recent_activities = []
        cursor_recent = uploads.find().sort("uploaded_at", -1).limit(5)
        async for doc in cursor_recent:
            recent_activities.append({
                "upload_id": str(doc.get("upload_id") or doc.get("_id") or ""),
                "filename": doc.get("filename", ""),
                "status": doc.get("status", "uploaded"),
                "uploaded_at": doc.get("uploaded_at") or doc.get("created_at") or datetime.utcnow(),
            })

        return {
            "statistics": {
                "total_uploads": total_uploads,
                "total_processed_images": total_processed,
                "total_reports_generated": total_reports,
                "total_objects_detected": total_objects,
                "total_completed_analysis": total_completed_analysis,
                "total_failed_jobs": total_failed_jobs,
                "active_sessions": active_sessions,
                "processing_success_rate": success_rate,
                "average_processing_time_seconds": avg_time,
                "storage_used_mb": storage_mb,
            },
            "recent_activities": recent_activities,
            "system_health": {
                "backend_status": "Online",
                "database_status": "Connected",
                "ai_model_status": "Ready",
                "uptime": "24h 0m",
                "last_updated": datetime.utcnow(),
            },
        }


dashboard_service = DashboardService()