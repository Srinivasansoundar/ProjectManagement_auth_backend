from src.data.repositories.user_repository import UserRepository
from src.schemas.user_schema import CreateUserRequest, UserResponse
from src.data.models.user import User
from src.core.exceptions.custom_exception import NotAdminException, ResourceNotFoundException, ConflictException, CustomException
from src.data.models.user import UserRole as ModelUserRole
from src.schemas.user_schema import CreateUserResponse,UserInfoResponse
from passlib.context import CryptContext
import logging
from uuid import UUID
logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class UserService:
    def __init__(self,user_repository:UserRepository):
        self.user_repository = user_repository
    async def create_user(self, payload: CreateUserRequest) -> CreateUserResponse:
        try:
            # check if user with email already exists
            existing = await self.user_repository.get_user_by_email(payload.email)
            if existing:
                raise ConflictException("User with this email already exists")

            # build user object (password hashing omitted for brevity)
            user = User(
                name=payload.name,
                email=payload.email,
                hashed_password=pwd_context.hash(payload.password),
                role=ModelUserRole(payload.role),
                created_by=payload.created_by,
                refresh_token=None
            )
            created = await self.user_repository.create_user(user)
            return CreateUserResponse(
                message="User created successfully",
                user=UserResponse(

                    id=created.id,
                    name=created.name,
                    email=created.email,
                    role=created.role
                )
            )
        except Exception as e:
            logger.error(f"Unexpected error creating user: {str(e)}")
            raise CustomException("Failed to create user", status_code=500)
    async def get_all_users(self):
        try:
            users = await self.user_repository.get_all_users()
            # Filter out admin users
            users = [user for user in users if user.role != ModelUserRole.ADMIN]
            return users
        except Exception as e:
            logger.error(f"Unexpected error fetching users: {str(e)}")
            raise CustomException("Failed to fetch users", status_code=500)
    async def get_user_info(self,user_id:UUID)->UserInfoResponse:
        try:
            user=await self.user_repository.get_user_by_id(user_id)
            if user is None:
                raise ResourceNotFoundException("User not found")
            return UserInfoResponse(
                id=user.id,
                name=user.name,
                email=user.email,
                role=user.role
            )
        except Exception as e:      
            logger.error(f"Unexpected error fetching user info: {str(e)}")
            raise CustomException("Failed to fetch user info", status_code=500)
    async def update_user_info(self,user_id:UUID,payload:CreateUserRequest)->UserInfoResponse:
        try:
            updated_user=await self.user_repository.update_user_info_by_id(user_id,payload)
            if updated_user is None:
                raise ResourceNotFoundException("User not found")
            return UserInfoResponse(
                id=updated_user.id,
                name=updated_user.name,
                email=updated_user.email,
                role=updated_user.role
            )
        except Exception as e:
            logger.error(f"Unexpected error updating user info: {str(e)}")
            raise CustomException("Failed to update user info", status_code=500)
    
    async def delete_user(self,user_id:UUID):
        try:
            deleted=await self.user_repository.delete_user_by_id(user_id)
            if not deleted:
                raise ResourceNotFoundException("User not found")
        except Exception as e:
            logger.error(f"Unexpected error deleting user: {str(e)}")
            raise CustomException("Failed to delete user", status_code=500)