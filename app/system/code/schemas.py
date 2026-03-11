from pydantic import Field

from app.common.schemas import CamelModel


class CodeGroupResponse(CamelModel):
    id: str
    name: str
    description: str | None = None
    is_active: bool = Field(alias="isActive")


class CodeResponse(CamelModel):
    id: str
    group_code: str = Field(alias="groupCode")
    code: str
    name: str
    value: str | None = None
    sort_order: int = Field(0, alias="sortOrder")
    is_active: bool = Field(alias="isActive")
    description: str | None = None


class CreateCodeRequest(CamelModel):
    group_code: str = Field(..., alias="groupCode")
    code: str
    name: str
    value: str | None = None
    sort_order: int = Field(0, alias="sortOrder")
    description: str | None = None


class UpdateCodeRequest(CamelModel):
    group_code: str = Field(..., alias="groupCode")
    name: str
    value: str | None = None
    sort_order: int = Field(0, alias="sortOrder")
    description: str | None = None
