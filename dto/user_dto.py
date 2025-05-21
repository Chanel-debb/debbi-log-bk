from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, Field


class TokenOtd(BaseModel):
    id: str


class LoginDto(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=6)]


class RegisterDto(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    password: Annotated[str, Field(min_length=6)]


class RefreshTokenDto(BaseModel):
    token: str


class Profile(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
