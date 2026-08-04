from fastapi import APIRouter, Depends, status

from dependencies.user import get_user_service
from schemas.users import UserCreate, UserResponse, UserUpdate
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/registration",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя",
)
async def create_user(
    user_data: UserCreate, service: UserService = Depends(get_user_service)  # noqa: B008
):
    user = await service.create_user(user_data)
    return user


@router.get(
    "/", response_model=list[UserResponse], summary="Получить список всех пользователей"
)
async def list_users(
    skip: int = 0,
    limit: int = 100,
    service: UserService = Depends(get_user_service),  # noqa: B008
):
    users = await service.get_users(skip=skip, limit=limit)
    return users


@router.get(
    "/{user_id}", response_model=UserResponse, summary="Получить пользователя по ID"
)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),  # noqa: B008
):
    user = await service.get_user(user_id)
    return user

@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Обновить пользователя"
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    service:  UserService = Depends(get_user_service),  # noqa: B008
):
    updated_user = await service.update_user(user_id, user_data)
    return updated_user

@router.delete("/{user_id}")
async def delete_event(user_id: int, service: UserService = Depends(get_user_service), summary="Удалить пользователя"):  # noqa: B008
    await service.delete_user(user_id=user_id)
    return {"message": "OK"}
