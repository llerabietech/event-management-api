from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from repositories.user_repository import UserRepository
from services.user_service import UserService


def get_user_repository(session: AsyncSession = Depends(get_db)) -> UserRepository:  # noqa: B008
    return UserRepository(session)


def get_user_service(
    repository: UserRepository = Depends(get_user_repository),  # noqa: B008
) -> UserService:
    return UserService(repository)


UserServiceDep = Annotated[
    UserService,
    Depends(get_user_service),
]

UserRepositoryDep = Annotated[
    UserRepository,
    Depends(get_user_repository),
]
