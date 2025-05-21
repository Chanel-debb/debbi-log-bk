from models.user_model import User
from dependencies.auth_dependencies import is_authenticated
from fastapi import APIRouter, Depends
from dto.user_dto import RegisterDto, LoginDto, RefreshTokenDto
from services.auth_sevice import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

auth_service = AuthService()


@router.post("/login", status_code=200)
async def login(dto: LoginDto):
    return await auth_service.login(dto)


@router.post("/register", status_code=201)
async def register(dto: RegisterDto):
    return await auth_service.register(dto)


@router.post("/refresh-token")
async def refresh_token(dto: RefreshTokenDto):
    return await auth_service.refresh_token(dto)


@router.get("/user", status_code=200)
async def get_user(current_user: User = Depends(is_authenticated)):
    return current_user