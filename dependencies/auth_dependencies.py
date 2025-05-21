from fastapi import Depends, HTTPException, status

from models.user_model import User
from services.auth_sevice import JwtService


async def admin_required(current_user: User = Depends(JwtService.get_current_user)):
    if current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action.",
        )
    return bool


async def is_authenticated(current_user: User = Depends(JwtService.get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authenticated"
        )
    return current_user