from fastapi import APIRouter, HTTPException

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

@router.delete("/{task_id}")
async def delete_event(id: int):
    pass