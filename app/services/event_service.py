from datetime import UTC, datetime

from app.core.permissions import can_manage_event
from app.exceptions import (
    EventAlreadyStartsError,
    EventNotFoundError,
)
from app.exceptions.base import PermissionDeniedError
from app.messaging.rabbitmq import RabbitClient
from app.models.users import User
from app.repositories.event_repository import EventRepository
from app.schemas.events import EventCreate, EventResponse, EventUpdate
from app.services.cache_service import CacheService


class EventService:
    def __init__(
        self,
        repository: EventRepository,
        cache: CacheService,
        rabbit: RabbitClient,
    ):
        self.repository = repository
        self.cache = cache
        self.rabbit = rabbit

    async def get_events(self, skip: int = 0, limit: int = 100):
        cache_key = "events:list"

        cached_events = await self.cache.get_json(cache_key)

        if cached_events is not None:
            return cached_events
        events = await self.repository.get_events(skip, limit)
        events_data = [
            EventResponse.model_validate(event).model_dump(mode="json")
            for event in events
        ]

        await self.cache.set_json(
            cache_key,
            events_data,
            ttl_seconds=60,
        )
        return events_data

    async def create_event(self, event_data: EventCreate, owner_id: int):
        event = await self.repository.create(event_data, owner_id)
        await self.rabbit.publish(
            routing_key="event.created",
            payload={
                "event_type": "event.created",
                "occurred_at": datetime.now(UTC).isoformat(),
                "data": {
                    "event_id": event.id,
                    "title": event.title,
                    "owner_id": event.owner_id,
                },
            },
        )
        await self.cache.delete("events:list")
        return event

    async def get_event(self, event_id: int):
        cache_key = f"events:{event_id}"

        cached_event = await self.cache.get_json(cache_key)

        if cached_event is not None:
            return cached_event
        event = await self.repository.get_event_by_id(event_id)
        if not event:
            raise EventNotFoundError(event_id)

        event_data = EventResponse.model_validate(event).model_dump(mode="json")

        await self.cache.set_json(
            cache_key,
            event_data,
            ttl_seconds=60,
        )

        return event_data

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
        await self.cache.delete("events:list")
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
        await self.cache.delete("events:list")
        return {"message": "OK"}
