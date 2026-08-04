from fastapi import APIRouter, Depends, HTTPException, status

from schemas.users import UserCreate, UserResponse, UserUpdate


class UserService:
    async def create_user(self, user_data: UserCreate):
        user = await self.repository.get_by_email(user_data.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

        user = await self.repository.create(user_data)

        return user
    
    async def get_users(self, skip: int = 0, limit: int = 100):
        users = await self.repository.get_users(skip, limit)
        return users
    
    async def get_user(self, user_id: int):
        user = await self.repository.get_user_by_id(user_id)
        if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
        return user
    
    async def update_user(self, user_id: int, user_data: UserUpdate):
        # Проверяем, существует ли пользователь
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Если обновляется email, проверяем уникальность
        if user_data.email and user_data.email != user.email:
            existing = await self.repository.get_by_email(user_data.email)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use"
                )
                
        updated_user = await self.repository.update(user_id, user_data)
        return updated_user
    
    async def delete_user(self, user_id: int):
        # Проверяем, существует ли пользователь
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Удаляем пользователя
        await self.repository.delete(user_id)
        return {"message": "OK"}