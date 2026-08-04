from schemas.users import UserCreate, UserResponse, UserUpdate

class UserRepository:
    async def get_by_email(self, email: str):
            pass
        
    async def create(self, user_data: UserCreate):
        pass
    
    async def get_users(self, skip: int = 0, limit: int = 100):
        pass
    
    async def get_user_by_id(self, user_id: int):
                pass
            
    async def update(self, user_id: int, user_data: UserUpdate):
            pass
    
    async def delete(self, user_id: int):
                pass
    
    