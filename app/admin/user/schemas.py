from pydantic import BaseModel, Field


class AdminUserResponse(BaseModel):
    id: str
    username: str
    name: str
    email: str | None = None
    phone: str | None = None
    role: str
    department: str | None = None
    position: str | None = None
    created_at: str | None = Field(None, alias="createdAt")
    is_active: bool = Field(alias="isActive")
    last_login_at: str | None = Field(None, alias="lastLoginAt")

    model_config = {"populate_by_name": True}


class CreateUserRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=4)
    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    role: str = Field(default="USER")
    department: str | None = None
    position: str | None = None


class UpdateUserRequest(BaseModel):
    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    role: str = Field(default="USER")
    department: str | None = None
    position: str | None = None
