from datetime import datetime

from fastapi import HTTPException, status

from repositories.event_repository import EventRepository
from schemas.events import EventCreate, EventUpdate


class EventService:
    def __init__(self, repository: EventRepository):
        self.repository = repository

    async def get_events(self, skip: int = 0, limit: int = 100):
        events = await self.repository.get_events(skip, limit)
        return events

    async def create_event(self, event_data: EventCreate):
        event = await self.repository.create(event_data)
        return event

    async def get_event(self, event_id: int):
        event = await self.repository.get_event_by_id(event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
            )
        return event

    async def update_event(self, event_id: int, event_data: EventUpdate):
        event = await self.repository.get_event_by_id(event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="event not found"
            )

        updated_event = await self.repository.update(event_id, event_data)
        return updated_event

    async def delete_event(self, event_id: int):
        event = await self.repository.get_event_by_id(event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="event not found"
            )

        if event.start_time <= datetime.utcnow():
            pass
            # TODO: raise EventAlreadyStarted()

        await self.repository.delete(event)
        # TODO: redis
        return {"message": "OK"}
