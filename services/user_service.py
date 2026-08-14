from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import verify_token
from app.exceptions import UserAlreadyExistsError, UserNotFoundError
from repositories.user_repository import UserRepository
from schemas.users import UserCreate, UserUpdate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user_data: UserCreate):
        user = await self.repository.get_by_email(user_data.email)
        if user:
            raise UserAlreadyExistsError()

        user = await self.repository.create(user_data)

        return user

    async def get_users(self, skip: int = 0, limit: int = 100):
        users = await self.repository.get_users(skip, limit)
        return users

    async def get_user(self, user_id: int):
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return user

    async def update_user(self, user_id: int, user_data: UserUpdate):
        # Проверяем, существует ли пользователь
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError()

        # Если обновляется email, проверяем уникальность
        if user_data.email and user_data.email != user.email:
            existing = await self.repository.get_by_email(user_data.email)
            if existing:
                raise UserAlreadyExistsError()

        updated_user = await self.repository.update(user_id, user_data)
        return updated_user

    async def delete_user(self, user_id: int):
        # Проверяем, существует ли пользователь
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        # Удаляем пользователя
        await self.repository.delete(user_id)
        return {"message": "OK"}

    async def get_current_user(self):
        token = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
        """Извлекает пользователя из JWT токена"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        payload = verify_token(token)
        if payload is None:
            raise credentials_exception

        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception

        try:
            user_id = int(user_id_str)
        except ValueError:
            raise credentials_exception

        user = await self.get_user(user_id)
        if user is None:
            raise credentials_exception

        return user
