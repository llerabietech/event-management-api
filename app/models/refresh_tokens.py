from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, PrimaryKeyConstraint, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.users import User


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_refresh_tokens"),
        Index("idx_refresh_tokens_jti", "jti", unique=True),
        Index("idx_refresh_tokens_user_id", "user_id"),
        Index("idx_refresh_tokens_user_revoked", "user_id", "revoked_at"),
        Index("idx_refresh_tokens_expires_at", "expires_at"),
        {
            "comment": "Хранит refresh-токены пользователей для продления сессии",
        },
    )

    id: Mapped[int] = mapped_column(comment="Идентификатор")
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="Идентификатор пользователя",
    )
    jti: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
        comment="Уникальный идентификатор токена (JWT ID)",
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        comment="Дата и время истечения срока действия токена",
    )
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Дата и время отзыва токена (пусто, если токен активен)",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Дата и время создания токена",
    )
    user: Mapped[User] = relationship(
        back_populates="refresh_tokens",
    )
