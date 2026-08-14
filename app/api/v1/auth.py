from fastapi import APIRouter, Response, status

from app.dependencies.auth import AuthServiceDep
from app.dependencies.user import UserServiceDep
from app.schemas.auth import (
    LoginRequest,
    RefreshRequest,
    TokenPair,
)
from app.schemas.users import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/registration",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя",
)
async def create_user(
    user_data: UserCreate,
    service: UserServiceDep,
):
    user = await service.create_user(user_data)
    return user


@router.post(
    "/login",
    response_model=TokenPair,
    status_code=status.HTTP_200_OK,
    summary="Вход пользователя",
)
async def login(
    data: LoginRequest,
    service: AuthServiceDep,
):
    return await service.login(data)


@router.post(
    "/refresh",
    response_model=TokenPair,
    status_code=status.HTTP_200_OK,
    summary="Обновление токенов",
)
async def refresh(
    data: RefreshRequest,
    service: AuthServiceDep,
):
    return await service.refresh(data)


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Выход пользователя",
)
async def logout(
    data: RefreshRequest,
    service: AuthServiceDep,
):
    await service.logout(data)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
