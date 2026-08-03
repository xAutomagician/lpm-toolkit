from fastapi import FastAPI

from app import config
from app.api.v1.router import api_router
from app.dataset import get_prefix_infos
from app.repository import InMemoryPrefixRepository


def create_app() -> FastAPI:
    app = FastAPI()
    app.state.config = config
    app.include_router(api_router, prefix="/api/v1")

    @app.on_event("startup")
    async def startup() -> None:
        app.state.prefix_repository = InMemoryPrefixRepository(get_prefix_infos())

    return app


app = create_app()
