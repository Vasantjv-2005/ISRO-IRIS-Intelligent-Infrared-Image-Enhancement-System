"""
MongoDB Index Configuration

This module creates indexes for the application's collections.
Indexes improve query performance and help enforce uniqueness
where required.
"""

from pymongo import ASCENDING

from app.database.mongodb import mongodb


async def create_indexes() -> None:
    """
    Create MongoDB indexes for all collections.
    """

    if mongodb.database is None:
        raise RuntimeError("MongoDB is not connected.")

    db = mongodb.database

    # ==========================
    # Uploads Collection
    # ==========================
    await db.uploads.create_index(
        [("filename", ASCENDING)],
        name="idx_filename"
    )

    await db.uploads.create_index(
        [("uploaded_at", ASCENDING)],
        name="idx_uploaded_at"
    )

    # ==========================
    # Reports Collection
    # ==========================
    await db.reports.create_index(
        [("created_at", ASCENDING)],
        name="idx_report_created_at"
    )

    # ==========================
    # Sessions Collection
    # ==========================
    await db.sessions.create_index(
        [("session_id", ASCENDING)],
        unique=True,
        name="idx_session_id"
    )

    # ==========================
    # Users Collection
    # ==========================
    await db.users.create_index(
        [("email", ASCENDING)],
        unique=True,
        name="idx_user_email"
    )
    await db.users.create_index(
        [("user_id", ASCENDING)],
        unique=True,
        name="idx_user_id"
    )

    # ==========================
    # Comparisons Collection
    # ==========================
    await db.comparisons.create_index(
        [("upload_id", ASCENDING)],
        unique=True,
        name="idx_comparison_upload_id"
    )

    # ==========================
    # Analyses Collection
    # ==========================
    await db.analyses.create_index(
        [("upload_id", ASCENDING)],
        name="idx_analysis_upload_id"
    )

    # ==========================
    # Images Collection
    # ==========================
    await db.images.create_index(
        [("upload_id", ASCENDING)],
        name="idx_image_upload_id"
    )

    print("MongoDB indexes created successfully.")