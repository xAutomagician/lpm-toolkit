import os
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

API_TOKEN_ENV = "API_TOKEN"
bearer_scheme = HTTPBearer(auto_error=False)


def get_api_token() -> str:
    token = os.getenv(API_TOKEN_ENV)
    if not token:
        raise RuntimeError(f"{API_TOKEN_ENV} is required")
    return token


def require_api_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> None:
    if credentials is None:
        raise _unauthorized()

    if credentials.scheme.lower() != "bearer":
        raise _unauthorized()

    if not secrets.compare_digest(credentials.credentials, get_api_token()):
        raise _unauthorized()


def _unauthorized() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API token",
        headers={"WWW-Authenticate": "Bearer"},
    )
