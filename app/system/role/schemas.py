from pydantic import BaseModel, Field


class RoleResponse(BaseModel):
    id: str
    name: str
    description: str | None = None


class CreateRoleRequest(BaseModel):
    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    description: str | None = None


class UpdateRoleRequest(BaseModel):
    name: str = Field(..., min_length=1)
    description: str | None = None
