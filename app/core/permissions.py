from app.models.events import Event
from app.models.users import User, UserRole

ROLE_LEVELS = {
    UserRole.USER: 1,
    UserRole.MODERATOR: 2,
    UserRole.ADMIN: 3,
}


def has_role_at_least(user_role: UserRole, required_role: UserRole) -> bool:
    """
    Проверяет, что роль пользователя не ниже требуемой.

    Например:
        ADMIN имеет доступ к MODERATOR и USER.
        MODERATOR имеет доступ к USER.
    """
    return ROLE_LEVELS[user_role] >= ROLE_LEVELS[required_role]


def can_manage_event(user: User, event: Event) -> bool:
    """
    Возвращает True, если пользователь может изменять/удалять событие.
    """
    if event.owner_id == user.id:
        return True

    return has_role_at_least(user.role, UserRole.MODERATOR)


def can_update_user(user_id: int, user: User) -> bool:
    """
    Возвращает True, если пользователь может изменять профиль.
    """
    if user_id == user.id:
        return True

    return has_role_at_least(user.role, UserRole.MODERATOR)
