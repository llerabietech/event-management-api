import json
from typing import Any

from redis.asyncio import Redis


class CacheService:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_json(self, key: str) -> Any | None:
        raw_value = await self.redis.get(key)

        if raw_value is None:
            return None

        return json.loads(raw_value)

    async def set_json(
        self,
        key: str,
        value: Any,
        ttl_seconds: int = 60,
    ) -> None:
        await self.redis.set(
            key,
            json.dumps(value),
            ex=ttl_seconds,
        )

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)

    async def delete_by_pattern(self, pattern: str) -> None:
        keys = []

        async for key in self.redis.scan_iter(match=pattern):
            keys.append(key)

        if keys:
            await self.redis.delete(*keys)
