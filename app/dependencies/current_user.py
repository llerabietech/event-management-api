from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_access_token
from app.dependencies import get_user_repository
from app.exceptions.auth import AccessTokenInvalidError
from app.models.users import User
from app.repositories.user_repository import UserRepository

http_bearer = HTTPBearer()


async def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(http_bearer),
    ],
    user_repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
):
    token = credentials.credentials

    payload = decode_access_token(token)

    user_id_str = payload.get("sub")

    if user_id_str is None:
        raise AccessTokenInvalidError()

    try:
        user_id = int(user_id_str)
    except ValueError:
        raise AccessTokenInvalidError()

    user = await user_repository.get_user_by_id(user_id)

    if user is None:
        raise AccessTokenInvalidError()

    return user


CurrentUserDep = Annotated[
    User,
    Depends(get_current_user),
]
