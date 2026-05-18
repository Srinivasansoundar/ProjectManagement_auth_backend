from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordBearer
from src.schemas.user_schema import(
     LoginRequest,
     LoginResponse,
     RefreshTokenRequest,
     RefreshTokenResponse)
from src.core.services.auth_service import AuthService
from src.api.rest.dependencies.services import get_auth_service

router=APIRouter(prefix="/auth",tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post(
    "/login",
    response_model=LoginResponse
)
async def login(
    payload:LoginRequest,
    auth_service:AuthService=Depends(get_auth_service)
    )->LoginResponse:
    response=await auth_service.login(payload)
    return response

@router.post(
    "/refresh",
    response_model=RefreshTokenResponse
)
async def refresh(
    payload:RefreshTokenRequest,
    auth_service:AuthService=Depends(get_auth_service)

)->RefreshTokenResponse:
    response=await auth_service.refresh(payload.refresh_token)
    return response
@router.post("/logout")
async def logout(
    access_token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.logout(access_token)