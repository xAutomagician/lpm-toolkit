from fastapi import FastAPI

from app.api.v1.auth import get_api_token
from app.api.v1.router import api_router
from app.repository import build_prefix_repository


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router, prefix="/api/v1")

    @app.on_event("startup")
    async def startup() -> None:
        get_api_token()
        app.state.prefix_repository = build_prefix_repository()

    return app


app = create_app()
