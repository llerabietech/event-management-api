from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession 

from app.models.events import Event
from app.schemas.events import EventCreate, EventUpdate


class EventRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_events(self, skip: int = 0, limit: int = 100) -> list[Event]:
        result = await self.db.execute(select(Event).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, event_data: EventCreate) -> Event:
        event = Event(
            title=event_data.title,
            description=event_data.description,
            location=event_data.location,
            start_time=event_data.start_time,
            end_time=event_data.end_time,
            capacity=event_data.capacity,
        )
        self.db.add(event)
        await self.db.flush()
        await self.db.refresh(event)
        return event

    async def get_event_by_id(self, event_id: int) -> Event | None:
        result = await self.db.execute(select(Event).where(Event.id == event_id))
        return result.scalar_one_or_none()

    async def update(self, event_id: int, event_data: EventUpdate) -> Event:
        event = await self.get_event_by_id(event_id)
        if not event:
            raise ValueError("event not found")

        update_data = event_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(event, field, value)

        await self.db.flush()
        await self.db.refresh(event)
        return event

    async def delete(self, event_id: int) -> None:
        event = await self.get_event_by_id(event_id)
        if not event:
            raise ValueError("event not found")

        await self.db.delete(event)
        await self.db.flush()
