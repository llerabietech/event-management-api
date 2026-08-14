from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_user_repository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService


def get_refresh_tokens_repository(
    session: AsyncSession = Depends(get_db),  # noqa: B008
) -> RefreshTokenRepository:
    return RefreshTokenRepository(session)


def get_auth_service(
    refresh_token_repository: RefreshTokenRepositoryDep,
    user_repository: UserRepository = Depends(get_user_repository),  # noqa: B008
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        refresh_token_repository=refresh_token_repository,
    )


AuthServiceDep = Annotated[
    AuthService,
    Depends(get_auth_service),
]

RefreshTokenRepositoryDep = Annotated[
    RefreshTokenRepository,
    Depends(get_refresh_tokens_repository),
]
