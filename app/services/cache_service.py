"""Сервис кэширования на базе Redis.

Предоставляет абстракцию над Redis-клиентом для работы
с JSON-данными. Используется для:
- Кэширования ответов сервисов (списки событий, профили пользователей)
- Временного хранения данных с автоматическим истечением (TTL)
- Инвалидации кэша по ключу или паттерну
"""
import json
from typing import Any

from redis.asyncio import Redis


class CacheService:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_json(self, key: str) -> Any | None:
        """Возвращает значение по ключу, десериализованное из JSON

        Args:
            key: Ключ кэша, например ``"app:events:list"``.

        Returns:
            Десериализованное Python-значение (словарь, список, число и т.д.)
            или ``None``, если ключ отсутствует.
        """
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
        """Сохраняет значение в кэш как JSON с заданным временем жизни

        Args:
            key: Ключ кэша, например ``"app:events:list"``.
            value: Любое JSON-сериализуемое значение
            ttl_seconds: Время жизни ключа в секундах

        """
        await self.redis.set(
            key,
            json.dumps(value),
            ex=ttl_seconds,
        )

    async def delete(self, key: str) -> None:
        """Удаляет один ключ из кэша.

        Args:
            key: Ключ кэша для удаления
        """
        await self.redis.delete(key)

    async def delete_by_pattern(self, pattern: str) -> None:
        """Удаляет все ключи, соответствующие паттерну.

        Паттерн использует синтаксис glob:
            - ``*`` — любое количество любых символов
            - ``?`` — один любой символ
            - ``[abc]`` — один символ из набора

        Args:
            pattern: Паттерн ключей, например:
                - ``"app:events:*"`` — все ключи событий
                - ``"app:users:1:*"`` — все ключи пользователя 1

        """
        keys = []

        async for key in self.redis.scan_iter(match=pattern):
            keys.append(key)

        if keys:
            await self.redis.delete(*keys)
