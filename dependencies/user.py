from fastapi import Depends
from repositories import user_repository as UserRepository
from services import user_service as UserService
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_db

def get_user_repository(session: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(session)

def get_user_service(
    repository: UserRepository = Depends(get_user_repository) 
) -> UserService:
    return UserService(repository)