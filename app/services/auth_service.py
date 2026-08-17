from datetime import UTC, datetime

from starlette.concurrency import run_in_threadpool

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    verify_password,
)
from app.exceptions.auth import (
    InvalidCredentialsError,
    RefreshTokenInvalidError,
)
from app.schemas.auth import LoginRequest, RefreshRequest, TokenPair


class AuthService:
    def __init__(
        self,
        user_repository,
        refresh_token_repository,
    ):
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository

    async def login(self, data: LoginRequest) -> TokenPair:
        user = await self.user_repository.get_by_email(
            data.username,
        )

        if user is None:
            raise InvalidCredentialsError()

        password_ok = await run_in_threadpool(
            verify_password,
            data.password,
            user.password_hash,
        )

        if not password_ok:
            raise InvalidCredentialsError()

        return await self._issue_tokens(user.id)

    async def refresh(self, data: RefreshRequest) -> TokenPair:
        payload = decode_refresh_token(data.refresh_token)

        record = await self.refresh_token_repository.get_by_jti(
            payload["jti"],
        )

        if record is None:
            raise RefreshTokenInvalidError()

        if record.revoked_at is not None:
            raise RefreshTokenInvalidError()

        now = datetime.now(UTC)

        if record.expires_at < now:
            raise RefreshTokenInvalidError()

        # Rotation: старый refresh token больше нельзя использовать.
        await self.refresh_token_repository.revoke_by_jti(record.jti)

        return await self._issue_tokens(record.user_id)

    async def logout(self, data: RefreshRequest) -> None:
        try:
            payload = decode_refresh_token(data.refresh_token)
        except RefreshTokenInvalidError:
            return

        await self.refresh_token_repository.revoke_by_jti(
            payload["jti"],
        )

    async def _issue_tokens(self, user_id: int) -> TokenPair:
        access_token = create_access_token(user_id)

        refresh_token, jti, expires_at = create_refresh_token(
            user_id,
        )

        await self.refresh_token_repository.create(
            user_id=user_id,
            jti=jti,
            expires_at=expires_at,
        )

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
        )
