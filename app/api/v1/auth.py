from fastapi import APIRouter, status

from app.dependencies.user import UserServiceDep
from app.schemas.users import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/registration",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя",
)
async def create_user(
    user_data: UserCreate,
    service: UserServiceDep,
):
    user = await service.create_user(user_data)
    return user

@router.post("/login")
def login():
    return {"message": "login"}


@router.post("/refresh")
def refresh():
    return {"message": "refresh"}


@router.post("/logout")
def logout():
    return {"message": "logout"}
