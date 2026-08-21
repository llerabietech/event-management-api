from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.dependencies.cache import CacheServiceDep
from app.repositories.event_repository import EventRepository
from app.services.event_service import EventService


def get_event_repository(session: AsyncSession = Depends(get_db)) -> EventRepository:  # noqa: B008
    return EventRepository(session)


def get_event_service(
    cache: CacheServiceDep,
    repository: EventRepository = Depends(get_event_repository),  # noqa: B008
) -> EventService:
    return EventService(repository, cache=cache)


EventServiceDep = Annotated[
    EventService,
    Depends(get_event_service),
]

EventRepositoryDep = Annotated[
    EventRepository,
    Depends(get_event_repository),
]
