from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.clients.postgress_client import get_async_db
from src.data.repositories.user_repository import UserRepository


async def get_user_repository(db: AsyncSession = Depends(get_async_db)) -> UserRepository:
	return UserRepository(db)
