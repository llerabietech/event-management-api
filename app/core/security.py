import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
import jwt
from fastapi import HTTPException, status
from jwt.exceptions import PyJWTError

from app.core.config import settings


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except ValueError, TypeError:
        return False


def create_token(subject: str, token_type: str) -> str:
    now = datetime.now(UTC)

    if token_type == "access":
        expires_at = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    elif token_type == "refresh":
        expires_at = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    else:
        raise ValueError("Unknown token type")

    payload = {
        "sub": subject,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
        "jti": str(uuid.uuid4()),
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_token(token: str, expected_type: str) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except PyJWTError:
        raise credentials_exception

    if payload.get("sub") is None:
        raise credentials_exception

    if payload.get("type") != expected_type:
        raise credentials_exception

    return payload

def verify_token(token: str) -> dict[str, Any] | None:
    try:
        # Декодируем токен с проверкой подписи и срока действия
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
        
    except jwt.ExpiredSignatureError:
        # Токен истёк
        return None
        
    except jwt.JWTError:
        # Любая другая ошибка JWT:
        # - Невалидная подпись
        # - Невалидный формат
        # - Невалидный алгоритм
        return None