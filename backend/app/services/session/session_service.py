"""
Session Service

Manages image processing sessions within the IRIS pipeline.
Adheres to Clean Architecture and SOLID principles by encapsulating business logic,
validating stage transitions and progress, and delegating persistence operations
to the SessionRepository.
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from app.models.session_model import (
    SessionModel,
    SessionStatus,
    utc_now,
)
from app.repositories.session_repository import session_repository
from app.schemas.session_schema import SessionResponseSchema
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


class SessionService:
    """
    Service responsible for managing image processing sessions.

    Encapsulates session lifecycle rules, progress validation, and error logging.
    Database interactions are strictly delegated to SessionRepository.
    """

    # =====================================================
    # Create Session
    # =====================================================

    async def create_session(
        self,
        db: Any,
        upload_id: str,
    ) -> SessionResponseSchema:
        """
        Create a new processing session for an uploaded image.

        Args:
            db:
                Database dependency parameter preserved for backward compatibility
                with public interface. Unused within this service as storage is
                managed by SessionRepository.
            upload_id:
                Unique identifier of the uploaded image associated with this session.

        Returns:
            SessionResponseSchema:
                The newly created session data schema.

        Raises:
            ValueError:
                If upload_id is empty or invalid.
            Exception:
                If database persistence fails.
        """
        if not upload_id or not upload_id.strip():
            raise ValueError("upload_id must be a non-empty string when creating a session.")

        logger.info("Creating new processing session for upload_id: %s", upload_id)

        try:
            now = utc_now()
            session = SessionModel(
                session_id=str(uuid4()),
                upload_id=upload_id.strip(),
                status=SessionStatus.CREATED,
                progress=0,
                current_stage="Upload",
                started_at=now,
                created_at=now,
                updated_at=now,
            )

            created_session = await session_repository.create(session)
            logger.info("Successfully created session: %s", created_session.session_id)

            return SessionResponseSchema.model_validate(created_session)

        except Exception as exc:
            logger.error("Failed to create session for upload_id %s: %s", upload_id, exc, exc_info=True)
            raise

    # =====================================================
    # Get Session
    # =====================================================

    async def get_session(
        self,
        db: Any,
        session_id: str,
    ) -> SessionResponseSchema | None:
        """
        Retrieve a session by its unique session ID.

        Args:
            db:
                Database dependency parameter preserved for API compatibility. Unused.
            session_id:
                Unique identifier of the processing session.

        Returns:
            SessionResponseSchema | None:
                The session schema if found, or None if the session does not exist.

        Raises:
            Exception:
                If database retrieval fails.
        """
        if not session_id or not session_id.strip():
            logger.warning("get_session called with empty session_id")
            return None

        logger.debug("Retrieving session by ID: %s", session_id)

        try:
            session = await session_repository.get_by_session_id(session_id.strip())
            if session is None:
                logger.debug("Session not found: %s", session_id)
                return None

            return SessionResponseSchema.model_validate(session)

        except Exception as exc:
            logger.error("Failed to retrieve session %s: %s", session_id, exc, exc_info=True)
            raise

    # =====================================================
    # Update Progress
    # =====================================================

    async def update_progress(
        self,
        db: Any,
        session_id: str,
        progress: int,
        current_stage: str,
    ) -> bool:
        """
        Update the progress percentage and current processing stage of a session.

        Args:
            db:
                Database dependency parameter preserved for API compatibility. Unused.
            session_id:
                Unique identifier of the processing session.
            progress:
                Progress value as an integer between 0 and 100.
            current_stage:
                Human-readable label of the current pipeline stage.

        Returns:
            bool:
                True if the session progress was successfully updated, False otherwise.

        Raises:
            ValueError:
                If progress is not within the valid range [0, 100] or session_id is empty.
            Exception:
                If database update fails.
        """
        if not 0 <= progress <= 100:
            raise ValueError(f"Progress must be between 0 and 100, received: {progress}")

        if not session_id or not session_id.strip():
            raise ValueError("session_id must be a non-empty string.")

        logger.debug("Updating progress for session %s: %d%% (%s)", session_id, progress, current_stage)

        try:
            updated = await session_repository.update_progress(
                session_id=session_id.strip(),
                progress=progress,
                current_stage=current_stage,
            )
            if not updated:
                logger.warning("Failed to update progress: session %s not found or unchanged", session_id)
            return updated

        except Exception as exc:
            logger.error("Error updating progress for session %s: %s", session_id, exc, exc_info=True)
            raise

    # =====================================================
    # Update Status
    # =====================================================

    async def update_status(
        self,
        db: Any,
        session_id: str,
        status: SessionStatus,
        error_message: str | None = None,
    ) -> bool:
        """
        Update the overall processing status of a session.

        Args:
            db:
                Database dependency parameter preserved for API compatibility. Unused.
            session_id:
                Unique identifier of the processing session.
            status:
                The new SessionStatus enum value.
            error_message:
                Optional descriptive error message if status is FAILED.

        Returns:
            bool:
                True if the status was successfully updated, False otherwise.

        Raises:
            ValueError:
                If session_id is empty or invalid.
            Exception:
                If database update fails.
        """
        if not session_id or not session_id.strip():
            raise ValueError("session_id must be a non-empty string.")

        logger.info("Updating status for session %s to %s", session_id, status.value)

        try:
            updated = await session_repository.update_status(
                session_id=session_id.strip(),
                status=status,
                error_message=error_message,
            )
            if not updated:
                logger.warning("Failed to update status: session %s not found or unchanged", session_id)
            return updated

        except Exception as exc:
            logger.error("Error updating status for session %s: %s", session_id, exc, exc_info=True)
            raise

    # =====================================================
    # Complete Session
    # =====================================================

    async def complete_session(
        self,
        db: Any,
        session_id: str,
        image_id: str | None = None,
        analysis_id: str | None = None,
        report_id: str | None = None,
        comparison_id: str | None = None,
        processing_time_seconds: float = 0.0,
    ) -> bool:
        """
        Mark a session as completed and associate generated entity IDs.

        Args:
            db:
                Database dependency parameter preserved for API compatibility. Unused.
            session_id:
                Unique identifier of the processing session.
            image_id:
                Optional ID of the processed image record.
            analysis_id:
                Optional ID of the AI analysis record.
            report_id:
                Optional ID of the generated report record.
            comparison_id:
                Optional ID of the image comparison record.
            processing_time_seconds:
                Total duration of pipeline execution in seconds.

        Returns:
            bool:
                True if the session was marked completed successfully, False otherwise.

        Raises:
            ValueError:
                If session_id is empty or invalid.
            Exception:
                If database update fails.
        """
        if not session_id or not session_id.strip():
            raise ValueError("session_id must be a non-empty string.")

        if processing_time_seconds < 0.0:
            processing_time_seconds = 0.0

        logger.info("Marking session as completed: %s (duration: %.2fs)", session_id, processing_time_seconds)

        try:
            completed = await session_repository.complete_session(
                session_id=session_id.strip(),
                image_id=image_id,
                analysis_id=analysis_id,
                report_id=report_id,
                comparison_id=comparison_id,
                processing_time_seconds=processing_time_seconds,
            )
            if not completed:
                logger.warning("Failed to mark completed: session %s not found or unchanged", session_id)
            return completed

        except Exception as exc:
            logger.error("Error completing session %s: %s", session_id, exc, exc_info=True)
            raise

    # =====================================================
    # Fail Session
    # =====================================================

    async def fail_session(
        self,
        db: Any,
        session_id: str,
        error_message: str,
    ) -> bool:
        """
        Mark a session as failed and record the failure reason.

        Args:
            db:
                Database dependency parameter preserved for API compatibility. Unused.
            session_id:
                Unique identifier of the processing session.
            error_message:
                Detailed explanation of the failure cause.

        Returns:
            bool:
                True if the session was updated to failed status, False otherwise.

        Raises:
            ValueError:
                If session_id is empty or invalid.
            Exception:
                If database update fails.
        """
        if not session_id or not session_id.strip():
            raise ValueError("session_id must be a non-empty string.")

        error_msg = error_message if error_message else "Unknown processing failure."
        logger.error("Marking session %s as failed: %s", session_id, error_msg)

        try:
            failed = await session_repository.fail_session(
                session_id=session_id.strip(),
                error_message=error_msg,
            )
            if not failed:
                logger.warning("Failed to mark failed status: session %s not found or unchanged", session_id)
            return failed

        except Exception as exc:
            logger.error("Error failing session %s: %s", session_id, exc, exc_info=True)
            raise

    # =====================================================
    # Delete Session
    # =====================================================

    async def delete_session(
        self,
        db: Any,
        session_id: str,
    ) -> bool:
        """
        Delete a session record from the database.

        Args:
            db:
                Database dependency parameter preserved for API compatibility. Unused.
            session_id:
                Unique identifier of the processing session to delete.

        Returns:
            bool:
                True if the session document was successfully deleted, False otherwise.

        Raises:
            ValueError:
                If session_id is empty or invalid.
            Exception:
                If database deletion fails.
        """
        if not session_id or not session_id.strip():
            raise ValueError("session_id must be a non-empty string.")

        logger.info("Deleting session record: %s", session_id)

        try:
            deleted = await session_repository.delete(session_id.strip())
            if deleted:
                logger.info("Successfully deleted session: %s", session_id)
            else:
                logger.warning("Session not found for deletion: %s", session_id)
            return deleted

        except Exception as exc:
            logger.error("Error deleting session %s: %s", session_id, exc, exc_info=True)
            raise

    # =====================================================
    # List Sessions
    # =====================================================

    async def list_sessions(
        self,
        db: Any,
        limit: int = 20,
    ) -> list[SessionResponseSchema]:
        """
        Retrieve a list of the most recent processing sessions.

        Args:
            db:
                Database dependency parameter preserved for API compatibility. Unused.
            limit:
                Maximum number of sessions to return (must be greater than 0).

        Returns:
            list[SessionResponseSchema]:
                List of recent session response schemas sorted by creation date.

        Raises:
            ValueError:
                If limit is less than 1.
            Exception:
                If database querying fails.
        """
        if limit < 1:
            raise ValueError(f"limit must be at least 1, received: {limit}")

        logger.debug("Listing up to %d recent processing sessions", limit)

        try:
            sessions = await session_repository.list_sessions(limit=limit)
            return [SessionResponseSchema.model_validate(session) for session in sessions]

        except Exception as exc:
            logger.error("Error listing recent sessions (limit=%d): %s", limit, exc, exc_info=True)
            raise


# ==========================================================
# Singleton
# ==========================================================

session_service = SessionService()