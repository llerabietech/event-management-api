from fastapi import APIRouter, Depends, status

from dependencies.user import get_user_service
from schemas.users import UserCreate, UserResponse
from services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/registration",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя",
)
async def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service),  # noqa: B008
):
    user = await service.create_user(user_data)
    return user

@router.post("/login")
def login():
    return {"message": "login"}


@router.post("/refresh")
def refresh():
    return {"message": "refresh"}


@router.post("/logout")
def logout():
    return {"message": "logout"}
