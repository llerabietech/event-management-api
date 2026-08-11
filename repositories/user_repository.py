from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from models.users import User
from schemas.users import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, user_data: UserCreate) -> User:
        user = User(
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role=user_data.role,
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def get_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        result = await self.db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_user_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def update(self, user_id: int, user_data: UserUpdate) -> User:
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        update_data = user_data.model_dump(exclude_unset=True)

        # Если обновляется пароль — хэшируем его
        if "password" in update_data:
            update_data["password_hash"] = hash_password(update_data.pop("password"))

        for field, value in update_data.items():
            setattr(user, field, value)

        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def delete(self, user_id: int) -> None:
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        await self.db.delete(user)
        await self.db.flush()
