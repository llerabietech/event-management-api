from fastapi import APIRouter

from app.dependencies.current_user import (
    CurrentAdminDep,
    CurrentModeratorDep,
    CurrentUserDep,
)
from app.dependencies.user import UserServiceDep
from app.schemas.users import UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=list[UserResponse], summary="Посмотреть свои данные")
async def get_me(service: UserServiceDep, user: CurrentUserDep):
    user = await service.get_user(user.id)
    return user


@router.get(
    "/", response_model=list[UserResponse], summary="Получить список всех пользователей"
)
async def list_users(
    service: UserServiceDep,
    admin: CurrentAdminDep,
    skip: int = 0,
    limit: int = 100,
):
    users = await service.get_users(skip=skip, limit=limit)
    return users


@router.get(
    "/{user_id}", response_model=UserResponse, summary="Получить пользователя по ID"
)
async def get_user(
    user_id: int, service: UserServiceDep, moderator: CurrentModeratorDep
):
    user = await service.get_user(user_id)
    return user


@router.patch(
    "/{user_id}", response_model=UserResponse, summary="Обновить пользователя"
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    service: UserServiceDep,
    current_user: CurrentUserDep,
):
    updated_user = await service.update_user(user_id, user_data, current_user)
    return updated_user


@router.delete("/{user_id}", summary="Удалить пользователя")
async def delete_event(
    user_id: int,
    service: UserServiceDep,
    admin: CurrentAdminDep,
):
    await service.delete_user(user_id=user_id)
    return {"message": "OK"}
