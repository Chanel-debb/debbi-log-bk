from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import decode, ExpiredSignatureError, InvalidTokenError, PyJWTError
from passlib.context import CryptContext

import env
from dto.user_dto import LoginDto, RefreshTokenDto, RegisterDto
from models.user_model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JwtService:
    @staticmethod
    async def generate_tokens(subject: str):
        access_expire = datetime.now(timezone.utc) + timedelta(
            minutes=env.JWT_ACCESS_EXPIRY
        )
        access_payload = {
            "sub": subject,
            "exp": access_expire,
        }
        access_token = jwt.encode(
            access_payload, env.JWT_ACCESS_SECRET, env.JWT_ALGORITHM
        )

        refresh_expire = datetime.now(timezone.utc) + timedelta(
            days=env.JWT_REFRESH_EXPIRY
        )
        refresh_payload = {
            "sub": subject,
            "exp": refresh_expire,
        }
        refresh_token = jwt.encode(
            refresh_payload, env.JWT_REFRESH_SECRET, env.JWT_ALGORITHM
        )

        return {"access_token": access_token, "refresh_token": refresh_token}

    @staticmethod
    async def get_current_user(
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    ) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = decode(
                token.credentials, env.JWT_ACCESS_SECRET, algorithms=[env.JWT_ALGORITHM]
            )
            user_id: str = payload.get("sub")
            if not user_id:
                raise credentials_exception
            user = await User.get_or_none(id=user_id)
            if user is None:
                raise credentials_exception
            return user
        except (ExpiredSignatureError, InvalidTokenError):
            raise credentials_exception


class AuthService:
    async def login(self, dto: LoginDto):
        user = await User.get_or_none(email=dto.email)
        if user is None:
            raise HTTPException(
                status_code=400,
                detail="No associated account with this email",
            )

        is_valid = pwd_context.verify(dto.password, user.password)
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail="Invalid credentials",
            )

        return await JwtService.generate_tokens(str(user.id))

    async def register(self, dto: RegisterDto):
        user = await User.get_or_none(email=dto.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="user with this email already exist",
            )

        dto.password = pwd_context.hash(dto.password)
        user = await User.create(**dto.model_dump())

        return await JwtService.generate_tokens(str(user.id))

    async def refresh_token(self, dto: RefreshTokenDto):
        return {}
