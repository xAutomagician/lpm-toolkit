from fastapi import FastAPI, Request

from app.api.v1.router import api_router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI()

    app.state

    app.include_router(api_router, prefix="/api/v1")

    @app.on_event("startup")
    async def startup():
        ...

    @app.on_event("shutdown")
    async def shutdown():
        ...

    return app


app = create_app()
