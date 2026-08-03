"""
Модуль зависимостей FastAPI.
Экспортирует все зависимости для использования в роутерах.
"""

from dependencies.database import get_db
from dependencies.event import (
    get_event_repository,
    get_event_service
)


__all__ = [
    # Database
    "get_db",
    # Event
    "get_event_repository",
    "get_event_service",
]