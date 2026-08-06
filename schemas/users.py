from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from models.users import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        max_length=72,
        description="Пароль должен быть от 8 до 72 символов",
    )
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    role: UserRole = Field(default=UserRole.USER)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=72,
        description="Пароль должен быть от 8 до 72 символов",
    )
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    role: UserRole | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole
    created_at: datetime
    updated_at: datetime
