import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from fastapi import FastAPI

from app.core.config import settings
from app.api.main import api_router
from app.core.redis import redis_client
from app.core.handlers import register_exception_handlers
from app.core.database import engine
from sqlalchemy import text

def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)
    app.include_router(api_router, prefix=settings.API_V1)

    @app.on_event("startup")
    async def startup():
        # contoh: ping redis
        await redis_client.ping()


    @app.on_event("shutdown")
    async def shutdown():
        await redis_client.close()

    @app.on_event("startup")
    async def startup():
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))

    register_exception_handlers(app)

    return app

app = create_app()