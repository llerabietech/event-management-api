from datetime import UTC, datetime

from app.core.permissions import can_manage_event
from app.exceptions import (
    EventAlreadyStartsError,
    EventNotFoundError,
)
from app.exceptions.base import PermissionDeniedError
from app.models.users import User
from app.repositories.event_repository import EventRepository
from app.schemas.events import EventCreate, EventUpdate


class EventService:
    def __init__(self, repository: EventRepository):
        self.repository = repository

    async def get_events(self, skip: int = 0, limit: int = 100):
        events = await self.repository.get_events(skip, limit)
        return events

    async def create_event(self, event_data: EventCreate, owner_id: int):
        event = await self.repository.create(event_data, owner_id)
        return event

    async def get_event(self, event_id: int):
        event = await self.repository.get_event_by_id(event_id)
        if not event:
            raise EventNotFoundError(event_id)
        return event

    async def update_event(
        self, event_id: int, event_data: EventUpdate, current_user: User
    ):
        event = await self.repository.get_event_by_id(event_id)
        if not event:
            raise EventNotFoundError(event_id)
        if not can_manage_event(current_user, event):
            raise PermissionDeniedError(
                "You can update only your own events",
            )

        updated_event = await self.repository.update(event_id, event_data)
        return updated_event

    async def delete_event(self, event_id: int, current_user: User):
        event = await self.repository.get_event_by_id(event_id)
        if not event:
            raise EventNotFoundError(event_id)

        if event.end_time >= datetime.now(UTC):
            raise EventAlreadyStartsError(event_id)

        if not can_manage_event(current_user, event):
            raise PermissionDeniedError(
                "You can delete only your own events",
            )

        await self.repository.delete(event_id)
        # TODO: redis
        return {"message": "OK"}
