from fastapi import APIRouter, Depends

from dependencies.event import get_event_service
from services.event_service import EventService

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

@router.get("/")
async def get_events():
    pass

@router.post("/")
async def create_event():
    pass

@router.delete("/{event_id}")
async def delete_event(event_id: int, service: EventService = Depends(get_event_service)):  # noqa: B008
    await service.delete_event(event_id=event_id)
    return {"message" : "OK"}