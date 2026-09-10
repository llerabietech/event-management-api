from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.users import User


class Event(Base):
    __tablename__ = "events"
    __table_args__ = (
            CheckConstraint(
                "end_time > start_time",
                name="ck_events_end_time_after_start_time",
            ),
            CheckConstraint(
                "capacity > 0",
                name="ck_events_capacity_positive",
            ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, comment="Идентификатор")
    title: Mapped[str] = mapped_column(String(254), nullable=False, comment="Название мероприятия")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="Описание мероприятия")
    location: Mapped[str] = mapped_column(String(255), nullable=False, comment="Местоположение")
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="Дата начала мероприятия"
    )
    end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="Дата окончания мероприятия"
    )
    capacity: Mapped[int] = mapped_column(nullable=False, comment="Количество человек")
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Идентификатор организатора"
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
    owner: Mapped[User] = relationship(
        back_populates="events",
    )
