from fastapi import Depends
from repositories import event_repository as EventRepository
from services import event_service as EventService
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db

def get_event_repository(session: AsyncSession = Depends(get_db)) -> EventRepository:
    return EventRepository(session)

def get_event_service(
    repository: EventRepository = Depends(get_event_repository) 
) -> EventService:
    return EventService(repository)