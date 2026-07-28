import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.api.v1.auth import get_api_token, require_api_token


def test_get_api_token_requires_env(monkeypatch):
    monkeypatch.delenv("API_TOKEN", raising=False)

    with pytest.raises(RuntimeError, match="API_TOKEN is required"):
        get_api_token()


def test_require_api_token_accepts_matching_bearer_token(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "secret-token")
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="secret-token",
    )

    assert require_api_token(credentials) is None


def test_require_api_token_rejects_invalid_token(monkeypatch):
    monkeypatch.setenv("API_TOKEN", "secret-token")
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="wrong-token",
    )

    with pytest.raises(HTTPException) as exc_info:
        require_api_token(credentials)

    assert exc_info.value.status_code == 401
