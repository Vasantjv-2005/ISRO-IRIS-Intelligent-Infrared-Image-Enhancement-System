"""
Auth Service & Endpoints Tests

Tests user account registration, password matching validation,
duplicate email handling, and JWT login using unit test mocks.
"""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.models.user_model import UserModel

client = TestClient(app)


@patch("app.services.auth.auth_service.user_repository")
def test_register_account_success(mock_repo):
    """
    Test successful account creation with full name, email, password, and confirm_password.
    """
    mock_repo.get_by_email = AsyncMock(return_value=None)
    
    fake_user = UserModel(
        user_id="user_12345",
        full_name="Test User Auth",
        email="testuser_auth@example.com",
        hashed_password="hashed_secret_password",
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )
    mock_repo.create = AsyncMock(return_value=fake_user)

    payload = {
        "full_name": "Test User Auth",
        "email": "testuser_auth@example.com",
        "password": "SecurePassword123!",
        "confirm_password": "SecurePassword123!",
    }

    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "testuser_auth@example.com"
    assert data["user"]["full_name"] == "Test User Auth"
    mock_repo.get_by_email.assert_called_once_with("testuser_auth@example.com")
    mock_repo.create.assert_called_once()


def test_register_account_password_mismatch():
    """
    Test that registration fails when password and confirm_password do not match.
    """
    payload = {
        "full_name": "Test User Auth",
        "email": "testuser_auth@example.com",
        "password": "SecurePassword123!",
        "confirm_password": "DifferentPassword123!",
    }

    response = client.post("/auth/register", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "VALIDATION_ERROR" in str(data) or "detail" in data


@patch("app.services.auth.auth_service.user_repository")
def test_register_duplicate_email(mock_repo):
    """
    Test that registering with an existing email returns 409 Conflict.
    """
    existing_user = UserModel(
        user_id="user_99999",
        full_name="Existing User",
        email="testuser_auth@example.com",
        hashed_password="hashed_password",
    )
    mock_repo.get_by_email = AsyncMock(return_value=existing_user)

    payload = {
        "full_name": "Test User Auth",
        "email": "testuser_auth@example.com",
        "password": "SecurePassword123!",
        "confirm_password": "SecurePassword123!",
    }

    response = client.post("/auth/register", json=payload)
    assert response.status_code == 409
    data = response.json()
    assert data["error"] == "CONFLICT"
    mock_repo.get_by_email.assert_called_once_with("testuser_auth@example.com")


@patch("app.services.auth.auth_service.user_repository")
@patch("app.services.auth.auth_service.AuthService.verify_password")
def test_login_account_success(mock_verify, mock_repo):
    """
    Test successful login after creating an account.
    """
    mock_verify.return_value = True
    
    fake_user = UserModel(
        user_id="user_12345",
        full_name="Test User Auth",
        email="testuser_auth@example.com",
        hashed_password="hashed_secret_password",
        is_active=True,
        created_at=datetime.now(timezone.utc),
    )
    mock_repo.get_by_email = AsyncMock(return_value=fake_user)

    login_payload = {
        "email": "testuser_auth@example.com",
        "password": "SecurePassword123!",
    }
    response = client.post("/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "testuser_auth@example.com"
    mock_repo.get_by_email.assert_called_once_with("testuser_auth@example.com")
    mock_verify.assert_called_once_with("SecurePassword123!", "hashed_secret_password")


@patch("app.services.auth.auth_service.user_repository")
@patch("app.services.auth.auth_service.AuthService.verify_password")
def test_login_account_wrong_password(mock_verify, mock_repo):
    """
    Test that login fails with incorrect password.
    """
    mock_verify.return_value = False
    
    fake_user = UserModel(
        user_id="user_12345",
        full_name="Test User Auth",
        email="testuser_auth@example.com",
        hashed_password="hashed_secret_password",
        is_active=True,
    )
    mock_repo.get_by_email = AsyncMock(return_value=fake_user)

    login_payload = {
        "email": "testuser_auth@example.com",
        "password": "WrongPassword!",
    }
    response = client.post("/auth/login", json=login_payload)
    assert response.status_code == 401
    data = response.json()
    assert data["error"] == "UNAUTHORIZED"
    mock_repo.get_by_email.assert_called_once_with("testuser_auth@example.com")
    mock_verify.assert_called_once_with("WrongPassword!", "hashed_secret_password")
