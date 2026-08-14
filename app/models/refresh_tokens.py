from datetime import datetime

import sqlalchemy.orm
from sqlalchemy import ForeignKey, String

from app.core.database import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(primary_key=True)

    user_id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    jti: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(
        String(36),
        unique=True,
        nullable=False,
        index=True,
    )

    expires_at: sqlalchemy.orm.Mapped[datetime] = sqlalchemy.orm.mapped_column(
        nullable=False
    )

    revoked_at: sqlalchemy.orm.Mapped[datetime | None] = sqlalchemy.orm.mapped_column(
        nullable=True
    )

    created_at: sqlalchemy.orm.Mapped[datetime] = sqlalchemy.orm.mapped_column(
        default=datetime.utcnow,
        nullable=False,
    )
