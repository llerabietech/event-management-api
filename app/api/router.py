from fastapi import APIRouter

from app.api.v1 import events, users

api_router = APIRouter()

api_router.include_router(events.router)
api_router.include_router(users.router)
