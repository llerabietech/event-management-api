import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from redis.asyncio import Redis

from app.api import router
from app.core.bootstrap import create_initial_admin
from app.core.config import settings
from app.core.error_handlers import register_error_handlers
from app.middleware import register_middleware

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаём админа при старте
    try:
        await create_initial_admin()
    except Exception as e:  # noqa: BLE001
        logger.error(f"Failed to create initial admin: {e}")
    try:
        app.state.redis = Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )
        await app.state.redis.ping()
        logger.info("Redis connected successfully")
    except Exception as e:  # noqa: BLE001
        logger.error(f"Redis connection failed: {e}")
        app.state.redis = None

    yield

    if app.state.redis is not None:
        await app.state.redis.aclose()
        logger.info("Redis disconnected")


app = FastAPI(
    title="Event Manager",
    description="",
    version="1.0.0",
    lifespan=lifespan,
)

register_error_handlers(app)
register_middleware(app)
app.include_router(router.api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Добро пожаловать в API! Перейдите на /docs для документации."}
