from src.core.exceptions.custom_exception import(
    ResourceNotFoundException,
    UnauthorizedException,
    CustomException
)
from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext
from uuid import UUID
from src.utils.decode_token import decode_token
from src.schemas.user_schema import LoginRequest
from src.config.settings import settings
import logging

logger =logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a plain text password using bcrypt."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        """Verify a plain text password against a hashed password."""
        return pwd_context.verify(plain, hashed)

    @staticmethod
    def create_access_token(data: dict) -> str:
        """Create a JWT token with expiration."""
        try:
            payload = data.copy()
            payload["exp"] = (
                datetime.utcnow()
                + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS)
            )
            return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        except JWTError as e:
            logger.error(f"Failed to create access token: {str(e)}")
            raise CustomException("Token creation failed", status_code=500)
    
    @staticmethod
    def create_refresh_token(data: dict):
        try:
            to_encode = data.copy()
            # data.copy() so that original copy is not modified
            expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
            to_encode.update({"exp": expire})
            return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        except JWTError as e:
            logger.error(f"Failed to create refresh token: {str(e)}")
            raise CustomException("Token creation failed", status_code=500)
    
    
    
    async def login(self,payload:LoginRequest):
        try:
            user=await self.user_repository.get_user_by_email(payload.email)
            if user is None:
                raise ResourceNotFoundException("Invalid email or password")
            
            verified=self.verify_password(payload.password,user.hashed_password if user else "dummy_hash")
            if user is None or not verified:
                raise UnauthorizedException("Invalid email or password")
            data={
                "sub":str(user.id),
                "role":user.role.value
            }
            access_token=self.create_access_token(data)
            refresh_token=self.create_refresh_token(data)
            await self.user_repository.update_refresh_token(user.id,refresh_token)
            logger.info(f"User {user.email} logged in successfully.")
            response={
                "access_token":access_token,
                "refresh_token":refresh_token,
                "token_type":"bearer",
                "user_info":{
                    "id":str(user.id),
                    "role":user.role.value
                }
            }
            return response
            
        except (ResourceNotFoundException,UnauthorizedException):
            raise
        except Exception as e:
            logger.error(f"Unexpected error during login: {str(e)}")
            raise CustomException("Failed to login", status_code=500)
    async def refresh(self,refresh_token:str):
        try:
            payload=decode_token(refresh_token)
            user_id_str=payload.get("sub")
            logger.info(f"Attempting to refresh token for user ID: {user_id_str}")
            try:
                user_id=UUID(user_id_str)  # Validate that user_id is a valid UUID
            except (ValueError, TypeError):
                raise UnauthorizedException("Invalid user ID in token")
            user=await self.user_repository.get_user_by_id(user_id)
            if user is None or str(user.refresh_token) != refresh_token:
                raise UnauthorizedException("Invalid refresh token")
            data={
                "sub":str(user.id),
                "role":user.role.value
            }
            new_access_token=self.create_access_token(data)
            new_refresh_token=self.create_refresh_token(data)
            await self.user_repository.update_refresh_token(user.id,new_refresh_token)
            logger.info(f"Refresh token for user {user.email} refreshed successfully.")
            return {
                "access_token":new_access_token,
                "refresh_token":new_refresh_token,
                "token_type":"bearer"
            }
       
        except UnauthorizedException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error during token refresh: {str(e)}")
            raise CustomException("Failed to refresh token", status_code=500)
    
    async def logout(self, access_token: str):
        """Invalidate refresh token on logout."""
        try:
            decoded = decode_token(access_token)
            user_id_str = decoded.get("sub")
            user_id=UUID(user_id_str)       
            await self.user_repository.update_refresh_token(user_id, None)
            logger.info(f"User {user_id} logged out successfully")
            return {"message": "Logout successful"}
        except (ValueError, TypeError):
            raise UnauthorizedException("Invalid user ID in token")
        except Exception as e:
            logger.error(f"Unexpected error during logout: {str(e)}")
            raise CustomException("Failed to logout", status_code=500)