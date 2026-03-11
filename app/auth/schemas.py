from pydantic import BaseModel, EmailStr, Field

from app.common.schemas import CamelModel


# Request
class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, description="사용자 ID")
    password: str = Field(..., min_length=1, description="비밀번호")


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="사용자 ID")
    password: str = Field(..., min_length=4, max_length=100, description="비밀번호")
    name: str = Field(..., min_length=1, description="이름")
    email: EmailStr = Field(..., description="이메일")


class RefreshRequest(CamelModel):
    refresh_token: str = Field(..., alias="refreshToken", description="리프레시 토큰")


# Response
class UserInfoResponse(BaseModel):
    id: str
    username: str
    name: str
    email: str
    role: str


class LoginResponse(CamelModel):
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")
    user: UserInfoResponse


class TokenResponse(CamelModel):
    access_token: str = Field(alias="accessToken")
