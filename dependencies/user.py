from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from repositories.user_repository import UserRepository
from services.user_service import UserService


def get_user_repository(session: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(session)

def get_user_service(
    repository: UserRepository = Depends(get_user_repository) 
) -> UserService:
    return UserService(repository)