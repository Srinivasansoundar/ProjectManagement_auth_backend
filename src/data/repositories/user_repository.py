from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from src.data.models.user import User

class UserRepository:
    def __init__(self,db:AsyncSession):
        self.db=db
    async def update_refresh_token(self,user_id:int,refresh_token:str)->None:
        result=await self.db.execute(select(User).where(User.id==user_id))
        user=result.scalar_one_or_none()
        if user:
            user.refresh_token=refresh_token
        # we don't need to flush as doing commit  will flush all changes
            
    async def create_user(self,user:User)->User:
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user
    async def get_user_by_email(self,email:str)->User | None:
        result=await self.db.execute(select(User).where(User.email==email))
        "Return exactly one object or None"
        return result.scalar_one_or_none()
    
    async def get_user_by_id(self, user_id) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
# Extract ORM objects from query result
# and return them as a list
    async def get_all_users(self):
        result = await self.db.execute(select(User))
        return result.scalars().all()
    
    async def update_user_info_by_id(self, user_id, payload) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            if hasattr(payload, 'name') and payload.name is not None:
                user.name = payload.name
            if hasattr(payload, 'email') and payload.email is not None:
                user.email = payload.email
            if hasattr(payload, 'role') and payload.role is not None:
                user.role = payload.role
            await self.db.flush()
            await self.db.refresh(user)
        return user
    
    
