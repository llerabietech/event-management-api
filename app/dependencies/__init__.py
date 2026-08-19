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

__all__ = [
    # Auth
    "get_auth_service",
    "get_current_user",
    # Database
    "get_db",
    # Event
    "get_event_repository",
    "get_event_service",
    "get_refresh_tokens_repository",
    # User
    "get_user_repository",
    "get_user_service",
    "require_role",
]
