from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class LoginHistoryResponse(BaseModel):
    login_ip: str | None = Field(None, alias="loginIp")
    login_success: bool = Field(alias="loginSuccess")
    login_fail_reason: str | None = Field(None, alias="loginFailReason")
    login_date: datetime | None = Field(None, alias="loginDate")
    model_config = {"populate_by_name": True}


# Request
class UpdateProfileRequest(BaseModel):
    name: str = Field(..., min_length=1, description="이름")
    email: EmailStr = Field(..., description="이메일")
    phone: str | None = Field(None, description="전화번호")


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., alias="currentPassword", min_length=1, description="현재 비밀번호")
    new_password: str = Field(..., alias="newPassword", min_length=4, max_length=100, description="새 비밀번호")


# Response
class UserProfileResponse(BaseModel):
    id: str
    username: str
    name: str
    email: str
    phone: str | None = None
    department: str | None = None
    position: str | None = None
    role: str
    created_at: datetime | None = Field(None, alias="createdAt")

    model_config = {"populate_by_name": True}
