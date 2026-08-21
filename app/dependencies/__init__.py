"""
Модуль зависимостей FastAPI.
Экспортирует все зависимости для использования в роутерах.
"""

from app.dependencies.database import get_db  # noqa: I001
from app.dependencies.event import (
    get_event_repository,
    get_event_service,
)
from app.dependencies.user import (
    get_user_repository,
    get_user_service,
)
from app.dependencies.auth import (
    get_auth_service,
    get_refresh_tokens_repository,
)
from app.dependencies.current_user import (
    get_current_user,
    require_role,
)
from app.dependencies.redis import (
    get_redis,
)
from app.dependencies.cache import (
    get_cache_service,
)

__all__ = [
    "get_auth_service",
    "get_cache_service",
    "get_current_user",
    "get_db",
    "get_event_repository",
    "get_event_service",
    "get_redis",
    "get_refresh_tokens_repository",
    "get_user_repository",
    "get_user_service",
    "require_role",
]
