"""
Модуль зависимостей FastAPI.
Экспортирует все зависимости для использования в роутерах.
"""

from app.dependencies.database import get_db
from app.dependencies.event import (
    get_event_repository,
    get_event_service,
)
from app.dependencies.user import (
    get_user_repository,
    get_user_service,
)


__all__ = [
    # Database
    "get_db",
    # Event
    "get_event_repository",
    "get_event_service",
    # User
    "get_user_repository",
    "get_user_service",
]