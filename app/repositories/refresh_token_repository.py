from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_tokens import RefreshToken


@dataclass
class RefreshTokenRecord:
    user_id: int
    jti: str
    expires_at: datetime
    revoked_at: datetime | None


class RefreshTokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        *,
        user_id: int,
        jti: str,
        expires_at: datetime,
    ) -> None:
        token = RefreshToken(
            user_id=user_id,
            jti=jti,
            expires_at=expires_at,
        )

        self.db.add(token)
        await self.db.commit()

    async def get_by_jti(self, jti: str) -> RefreshTokenRecord | None:
        query = select(RefreshToken).where(RefreshToken.jti == jti)

        result = await self.db.execute(query)
        token = result.scalar_one_or_none()

        if token is None:
            return None

        return RefreshTokenRecord(
            user_id=token.user_id,
            jti=token.jti,
            expires_at=token.expires_at,
            revoked_at=token.revoked_at,
        )

    async def revoke_by_jti(self, jti: str) -> None:
        query = (
            update(RefreshToken)
            .where(RefreshToken.jti == jti)
            .values(revoked_at=datetime.now(UTC))
        )

        await self.db.execute(query)
        await self.db.commit()
