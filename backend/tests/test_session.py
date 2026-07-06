"""
Tests for Session Service and Controller.
"""

from __future__ import annotations

from datetime import datetime
import unittest
from unittest.mock import AsyncMock, patch

from app.models.session_model import SessionModel, SessionStatus
from app.controllers.session_controller import session_controller


class TestSessionService(unittest.IsolatedAsyncioTestCase):
    """
    Tests for SessionService operations.
    """

    @patch("app.services.session.session_service.session_repository")
    async def test_create_session_success(
        self,
        mock_session_repo: AsyncMock,
    ) -> None:
        """
        Verify session creation succeeds for an existing upload.
        """

        mock_session_repo.create = AsyncMock(
            return_value=SessionModel(
                session_id="session_123",
                upload_id="upload_123",
                status=SessionStatus.CREATED,
                started_at=datetime.utcnow(),
            )
        )

        res = await session_controller.create_session(db=None, upload_id="upload_123")
        self.assertEqual(res.session_id, "session_123")
        self.assertEqual(res.upload_id, "upload_123")
        self.assertEqual(res.status, SessionStatus.CREATED)
