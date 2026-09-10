"""Сервис управления пользователями.

Реализует бизнес-логику работы с учётными записями:
- Создание пользователей с проверкой уникальности email
- Получение списка пользователей и отдельных записей
- Обновление профиля с проверкой прав доступа
- Удаление пользователей
"""

from app.core.permissions import can_update_user
from app.exceptions import (
    PermissionDeniedError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.models.users import User
from app.repositories.user_repository import UserRepository
from app.schemas.users import UserCreate, UserUpdate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user_data: UserCreate):
        """Создаёт нового пользователя с проверкой уникальности email.

        Args:
            user_data: Данные нового пользователя::

                {
                    "email": "alice@example.com",
                    "password": "secret",
                    "first_name": "Alice",
                    "last_name": "Smith"
                }

        Returns:
            Созданная модель пользователя с присвоенным ``id``
            и хешированным паролем
        """
        user = await self.repository.get_by_email(user_data.email)
        if user:
            raise UserAlreadyExistsError(user_data.email)

        user = await self.repository.create(user_data)

        return user

    async def get_users(self, skip: int = 0, limit: int = 100):
        """Возвращает список пользователей с поддержкой пагинации.


        Args:
            skip: Количество записей, которые нужно пропустить
            limit: Максимальное количество возвращаемых записей

        Returns:
            Список моделей пользователей
        """
        users = await self.repository.get_users(skip, limit)
        return users

    async def get_user(self, user_id: int):
        """Возвращает пользователя по идентификатору."""
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return user

    async def get_user_by_email(self, user_email: str):
        """Возвращает пользователя по email-адресу."""
        user = await self.repository.get_user_by_email(user_email)
        if not user:
            raise UserNotFoundError(user_email)
        return user

    async def update_user(
        self, user_id: int, user_data: UserUpdate, current_user: User
    ):
        """Обновляет профиль пользователя с проверкой прав и уникальности.

        Args:
            user_id: Идентификатор обновляемого пользователя.
            user_data: Поля для обновления (частичное обновление —
                только переданные поля будут изменены)::

                    {
                        "first_name": "Alice",
                        "email": "new@example.com"
                    }

            current_user: Текущий аутентифицированный пользователь,
                передаётся из зависимости ``CurrentUserDep``.

        Returns:
            Обновлённая модель пользователя.

        """
        if not can_update_user(user_id, current_user):
            raise PermissionDeniedError(
                "You can update only your profile",
            )
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
        """Удаляет пользователя по идентификатору.

        Args:
            user_id: Идентификатор удаляемого пользователя

        Returns:
            Сообщение об успешном удалении::

                {"message": "OK"}
        """
        # Проверяем, существует ли пользователь
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        # Удаляем пользователя
        await self.repository.delete(user_id)
        return {"message": "OK"}
