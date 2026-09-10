"""Модуль безопасности: хеширование паролей и JWT-токены.

Реализует:
- Хеширование паролей через bcrypt
- Создание и валидацию JWT access-токенов (короткое время жизни)
- Создание и валидацию JWT refresh-токенов (длительное время жизни)

JWT payload содержит поля:
- ``sub`` — идентификатор пользователя
- ``type`` — тип токена ("access" или "refresh")
- ``iat`` — время создания (issued at)
- ``exp`` — время истечения (expiration)
- ``jti`` — уникальный идентификатор токена (JWT ID)

Конфигурация через переменные окружения:
- ``JWT_SECRET_KEY`` — секретный ключ для подписи
- ``ALGORITHM`` — алгоритм подписи (по умолчанию HS256)
- ``ACCESS_TOKEN_EXPIRE_MINUTES`` — время жизни access-токена
- ``REFRESH_TOKEN_EXPIRE_DAYS`` — время жизни refresh-токена
"""

import os
import uuid
from datetime import UTC, datetime, timedelta

import bcrypt
import jwt
from jwt.exceptions import PyJWTError

from app.exceptions.auth import (
    AccessTokenInvalidError,
    RefreshTokenInvalidError,
)

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))

REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))


def hash_password(password: str) -> str:
    """Хеширует пароль с помощью bcrypt.
    Args:
        password: Пароль в открытом виде.

    Returns:
        Хешированный пароль в формате bcrypt
    """
    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(rounds=12),
    )

    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """Проверяет соответствие пароля его хешу.

    Args:
        password: Пароль в открытом виде для проверки.
        hashed_password: Сохранённый хеш bcrypt.

    Returns:
        True, если пароль соответствует хешу, иначе False.
        Возвращает False также при невалидном формате хеша
    """
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except ValueError, TypeError:
        return False


def create_access_token(user_id: int) -> str:
    """Создаёт access JWT-токен для авторизации пользователя.

    Args:
        user_id: Идентификатор пользователя

    Returns:
        Закодированная строка JWT-токена
    """
    now = datetime.now(UTC)
    expires_at = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
        "jti": str(uuid.uuid4()),
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def create_refresh_token(user_id: int) -> tuple[str, str, datetime]:
    """Создаёт refresh JWT-токен для обновления access-токена.

    Args:
        user_id: Идентификатор пользователя

    Returns:
        Кортеж из трёх элементов:
            - ``token`` — закодированная строка refresh JWT-токена
            - ``jti`` — уникальный идентификатор токена (для сохранения в БД)
            - ``expires_at`` — время истечения токена (datetime с timezone)
    """
    now = datetime.now(UTC)
    expires_at = now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    jti = str(uuid.uuid4())

    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
        "jti": jti,
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return token, jti, expires_at


def _decode_token(token: str, expected_type: str) -> dict:
    """Декодирует и валидирует JWT-токен

    Args:
        token: Закодированная строка JWT-токена.
        expected_type: Ожидаемый тип токена — ``"access"`` или ``"refresh"``.

    Returns:
        Словарь с полями payload токена при успешной валидации.
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except PyJWTError:
        if expected_type == "access":
            raise AccessTokenInvalidError()

        raise RefreshTokenInvalidError()

    if payload.get("sub") is None:
        if expected_type == "access":
            raise AccessTokenInvalidError()

        raise RefreshTokenInvalidError()

    if payload.get("type") != expected_type:
        if expected_type == "access":
            raise AccessTokenInvalidError()

        raise RefreshTokenInvalidError()

    return payload


def decode_access_token(token: str) -> dict:
    """Декодирует и валидирует access JWT-токен.

    Публичная обёртка над ``_decode_token`` для access-токенов.
    Проверяет подпись, срок действия и тип токена.

    Args:
        token: Закодированная строка access-токена.

    Returns:
        Словарь с полями payload
    """
    return _decode_token(token, expected_type="access")


def decode_refresh_token(token: str) -> dict:
    """Декодирует и валидирует refresh JWT-токен.

    Публичная обёртка над ``_decode_token`` для refresh-токенов.
    Проверяет подпись, срок действия и тип токена.

    Args:
        token: Закодированная строка refresh-токена.

    Returns:
        Словарь с полями payload
    """
    return _decode_token(token, expected_type="refresh")
