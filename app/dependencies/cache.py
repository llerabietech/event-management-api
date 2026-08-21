from typing import Annotated

from fastapi import Depends

from app.dependencies.redis import RedisDep
from app.services.cache_service import CacheService


def get_cache_service(redis: RedisDep) -> CacheService:
    return CacheService(redis)


CacheServiceDep = Annotated[
    CacheService,
    Depends(get_cache_service),
]