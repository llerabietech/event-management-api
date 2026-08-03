from fastapi import APIRouter, Depends

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
async def delete_event(event_id: int, service: Depends(get_event_service)):
    await service.delete_event(event_id=event_id)
    return {"message" : "OK"}