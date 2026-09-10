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
    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(rounds=12),
    )

    return hashed.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except ValueError, TypeError:
        return False


def create_access_token(user_id: int) -> str:
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
    return _decode_token(token, expected_type="access")


def decode_refresh_token(token: str) -> dict:
    return _decode_token(token, expected_type="refresh")
