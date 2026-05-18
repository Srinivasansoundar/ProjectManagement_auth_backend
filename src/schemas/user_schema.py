from pydantic import BaseModel
from uuid import UUID
from src.data.models.user import UserRole
class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str
    created_by:UUID
class UserResponse(BaseModel):
    id: UUID
    email: str
    role: UserRole
class CreateUserResponse(BaseModel):
    message: str
    user: UserResponse


class LoginRequest(BaseModel):
     email:str
     password:str

class LoginResponse(BaseModel):
    access_token:str
    refresh_token:str
    token_type:str="bearer"
    user_info:dict

class UserInfoResponse(BaseModel):
    id: UUID
    name:str
    email: str
    role: UserRole

class RefreshTokenRequest(BaseModel):
    refresh_token: str
class RefreshTokenResponse(BaseModel):
    refresh_token: str
    access_token: str
    token_type: str = "bearer"