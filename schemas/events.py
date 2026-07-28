from datetime import datetime

from pydantic import BaseModel, Field

class Event(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=100,
        examples="Python Meetup Moscow",
    )
    description: str | None = Field(
        default=None,
        examples="Митап для Python-разработчиков в Москве",
        max_length=1000,
    )
    location: str | None = Field(
        default=None,
        max_length=500,
        examples="г. Москва, ул. Тверская, д.5",
    )
    start_time: datetime = Field(
        description="Дата начала события",
    )
    end_time: datetime = Field(
        description="Дата окончания события",
    )
    capacity: int = Field(
        description="Максимальное количество учвстников",
        gt=0,
        le=10000,
    )