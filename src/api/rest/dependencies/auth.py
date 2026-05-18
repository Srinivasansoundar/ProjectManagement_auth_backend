from jose import jwt, JWTError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.config.settings import settings
from src.core.exceptions.custom_exception import (
    UnauthorizedException,CustomException
)   

from src.utils.decode_token import decode_token
import logging
logger = logging.getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
async def verify_admin(
        token:str=Depends(oauth2_scheme)
    ):
    """Verify user has admin role."""
    payload = decode_token(token)  # Already handles JWT errors
    role = payload.get("role")
    if role != "admin":
        raise UnauthorizedException("Admin privileges required")
    return




