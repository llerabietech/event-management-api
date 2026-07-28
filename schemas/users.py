from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    email: EmailStr = Field(
        description="Email для пользователя",
    )
    first_name: str = Field(
        description="Имя пользователя"
    )
    last_name: str = Field(
        description="Фамилия пользователя"
    )
    role: list[str] = Field(
        description="Роль пользователя"
    )