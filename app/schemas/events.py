from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.exceptions import EventEndTimeError


class EventBase(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=254,
        examples=["Python Meetup Moscow"]
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        examples=["Митап для Python-разработчиков в Москве"]
    )
    location: str | None = Field(
        default=None,
        max_length=255,
        examples=["г. Москва, ул. Тверская, д.5"]
    )
    start_time: datetime = Field(description="Дата начала события")
    end_time: datetime = Field(description="Дата окончания события")
    capacity: int = Field(
        description="Максимальное количество участников",
        gt=0,
        le=10000
    )
@model_validator(mode="after")
def validate_event_time(self):
    if self.end_time <= self.start_time:
        raise EventEndTimeError()

    return self

class EventCreate(EventBase):
    pass 

class EventUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=254)
    description: str | None = Field(default=None, max_length=1000)
    location: str | None = Field(default=None, max_length=255)
    start_time: datetime | None = None
    end_time: datetime | None = None
    capacity: int | None = Field(default=None, gt=0, le=10000)

class EventResponse(EventBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime