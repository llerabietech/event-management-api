from app.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.repositories.user_repository import UserRepository
from app.schemas.users import UserCreate, UserUpdate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user_data: UserCreate):
        user = await self.repository.get_by_email(user_data.email)
        if user:
            raise UserAlreadyExistsError(user_data.email)

        user = await self.repository.create(user_data)

        return user

    async def get_users(self, skip: int = 0, limit: int = 100):
        users = await self.repository.get_users(skip, limit)
        return users

    async def get_user(self, user_id: int):
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return user

    async def get_user_by_email(self, user_email: str):
        user = await self.repository.get_user_by_email(user_email)
        if not user:
            raise UserNotFoundError(user_email)
        return user

    async def update_user(self, user_id: int, user_data: UserUpdate):
        # Проверяем, существует ли пользователь
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)

        # Если обновляется email, проверяем уникальность
        if user_data.email and user_data.email != user.email:
            existing = await self.repository.get_by_email(user_data.email)
            if existing:
                raise UserAlreadyExistsError(user_data.email)

        updated_user = await self.repository.update(user_id, user_data)
        return updated_user

    async def delete_user(self, user_id: int):
        # Проверяем, существует ли пользователь
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        # Удаляем пользователя
        await self.repository.delete(user_id)
        return {"message": "OK"}
