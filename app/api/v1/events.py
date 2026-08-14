from fastapi import APIRouter, status

from dependencies.event import EventServiceDep
from schemas.events import EventCreate, EventResponse, EventUpdate

router = APIRouter(prefix="/events", tags=["Events"])


@router.post(
    "/",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Добавление нового события",
)
async def create_event(
    event_data: EventCreate,
    service: EventServiceDep,
):
    event = await service.create_event(event_data)
    return event


@router.get(
    "/", response_model=list[EventResponse], summary="Получить список всех событий"
)
async def get_events(
    service: EventServiceDep,
    skip: int = 0,
    limit: int = 100,
):
    events = await service.get_events(skip=skip, limit=limit)
    return events


@router.get(
    "/{event_id}", response_model=EventResponse, summary="Получить событие по ID"
)
async def get_event(
    event_id: int,
    service: EventServiceDep,
):
    event = await service.get_event(event_id)
    return event


@router.patch("/{event_id}", response_model=EventResponse, summary="Обновить событие")
async def update_event(
    event_id: int,
    event_data: EventUpdate,
    service: EventServiceDep,
):
    updated_event = await service.update_event(event_id, event_data)
    return updated_event


@router.delete("/{event_id}", summary="Удалить событие")
async def delete_event(
    event_id: int,
    service: EventServiceDep,
):
    await service.delete_event(event_id=event_id)
    return {"message": "OK"}
