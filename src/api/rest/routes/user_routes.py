from fastapi import APIRouter, Depends, status,Path
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from src.schemas.user_schema import(
     CreateUserRequest,
     CreateUserResponse,
     UserResponse,
     UserInfoResponse,
     UpdateUserRequest)
from src.api.rest.dependencies.services import get_user_service
from src.api.rest.dependencies.auth import verify_admin
from src.core.services.user_service import UserService
from typing import List
from uuid import UUID
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post(
    "/user",
    response_model=CreateUserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    payload: CreateUserRequest,
    _:None=Depends(verify_admin),
    user_service: UserService = Depends(get_user_service),
):

    response = await user_service.create_user(payload)

    return response

@router.get(
    "/users",
    response_model=List[UserResponse]
)
async def get_all_users(
    _:None=Depends(verify_admin),
    user_service: UserService = Depends(get_user_service),
):
    res = await user_service.get_all_users()
    return res

@router.get(
    "/user/{user_id}",
    response_model=UserInfoResponse
)
async def get_user_info(
    user_id:UUID=Path(..., description="User ID"),
    user_service:UserService=Depends(get_user_service)
):
    res=await user_service.get_user_info(user_id)
    return res

@router.put(
    "/user/{user_id}",
    response_model=UserInfoResponse,
    status_code=status.HTTP_200_OK
)
async def update_user_info(
    user_id:UUID=Path(..., description="User ID"),
    payload:UpdateUserRequest=None,
    _:None=Depends(verify_admin),
    user_service:UserService=Depends(get_user_service)      
):
    res=await user_service.update_user_info(user_id,payload)
    return res

@router.delete(
    "/user/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
    user_id:UUID=Path(..., description="User ID"),
    _:None=Depends(verify_admin),
    user_service:UserService=Depends(get_user_service)      
):
    await user_service.delete_user(user_id)
