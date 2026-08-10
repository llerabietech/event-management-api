from fastapi import APIRouter, Depends, status

from dependencies.event import get_event_service
from schemas.events import EventCreate, EventResponse, EventUpdate
from services.event_service import EventService

router = APIRouter(prefix="/events", tags=["Events"])


@router.post(
    "/",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Добавление нового события",
)
async def create_event(
    event_data: EventCreate,
    service: EventService = Depends(get_event_service),  # noqa: B008
):
    event = await service.create_event(event_data)
    return event


@router.get(
    "/", response_model=list[EventResponse], summary="Получить список всех событий"
)
async def get_events(
    skip: int = 0,
    limit: int = 100,
    service: EventService = Depends(get_event_service),  # noqa: B008
):
    events = await service.get_events(skip=skip, limit=limit)
    return events


@router.get(
    "/{event_id}", response_model=EventResponse, summary="Получить событие по ID"
)
async def get_event(
    event_id: int,
    service: EventService = Depends(get_event_service),  # noqa: B008
):
    event = await service.get_event(event_id)
    return event


@router.patch("/{event_id}", response_model=EventResponse, summary="Обновить событие")
async def update_event(
    event_id: int,
    event_data: EventUpdate,
    service: EventService = Depends(get_event_service),  # noqa: B008
):
    updated_event = await service.update_event(event_id, event_data)
    return updated_event


@router.delete("/{event_id}", summary="Удалить событие")
async def delete_event(
    event_id: int,
    service: EventService = Depends(get_event_service),  # noqa: B008
):
    await service.delete_event(event_id=event_id)
    return {"message": "OK"}
