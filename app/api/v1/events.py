from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/events",
    tags=["События"]
)

fake_database =[]