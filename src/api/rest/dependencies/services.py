from fastapi import Depends

from src.api.rest.dependencies.repositories import get_user_repository
from src.core.services.user_service import UserService
from src.core.services.auth_service import AuthService

async def get_user_service(user_repository=Depends(get_user_repository)) -> UserService:
	return UserService(user_repository)
async def get_auth_service(user_repository=Depends(get_user_repository)) -> AuthService:
	return AuthService(user_repository)

