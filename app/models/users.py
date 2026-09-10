from datetime import datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.events import Event
    from app.models.refresh_tokens import RefreshToken


class UserRole(str, PyEnum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, comment="Идентификатор")
    email: Mapped[str] = mapped_column(
        String(254),
        unique=True,
        index=True,
        nullable=False,
        comment="Email"
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Хэш пароля"
    )
    first_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="Имя")
    last_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="Фамилия")
    role: Mapped[UserRole] = mapped_column(
        SAEnum(
            UserRole,
            name="user_role",
            native_enum=False,
            length=20,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        default=UserRole.USER,
        server_default=UserRole.USER.value,
        nullable=False,
        comment="Роль пользователя"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Дата создания"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Дата обновления"
    )
    events: Mapped[list[Event]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
    )
    refresh_tokens: Mapped[list[RefreshToken]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
