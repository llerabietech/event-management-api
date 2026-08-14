from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.security import decode_access_token
from app.dependencies import get_user_repository
from app.exceptions.auth import AccessTokenInvalidError
from app.models.users import User
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_repository: UserRepository = Depends(get_user_repository),  # noqa: B008,
):
    """
    Извлекает пользователя из JWT access токена.
    """
    payload = decode_access_token(token)

    user_id_str = payload.get("sub")

    if user_id_str is None:
        raise AccessTokenInvalidError()

    try:
        user_id = int(user_id_str)
    except ValueError:
        raise AccessTokenInvalidError()

    user = await user_repository.get_by_id(user_id)

    if user is None:
        raise AccessTokenInvalidError()

    return user


CurrentUserDep = Annotated[
    User,
    Depends(get_current_user),
]
