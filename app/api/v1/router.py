from fastapi import APIRouter

from app.api.v1 import lookup


api_router = APIRouter()
api_router.include_router(lookup.router)

__all__ = ["api_router"]
