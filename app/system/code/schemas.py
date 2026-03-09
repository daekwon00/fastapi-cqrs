from pydantic import BaseModel, Field


class CodeGroupResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    is_active: bool = Field(alias="isActive")
    model_config = {"populate_by_name": True}


class CodeResponse(BaseModel):
    id: str
    group_code: str = Field(alias="groupCode")
    code: str
    name: str
    value: str | None = None
    sort_order: int = Field(0, alias="sortOrder")
    is_active: bool = Field(alias="isActive")
    description: str | None = None
    model_config = {"populate_by_name": True}


class CreateCodeRequest(BaseModel):
    group_code: str = Field(..., alias="groupCode")
    code: str
    name: str
    value: str | None = None
    sort_order: int = Field(0, alias="sortOrder")
    description: str | None = None
    model_config = {"populate_by_name": True}


class UpdateCodeRequest(BaseModel):
    group_code: str = Field(..., alias="groupCode")
    name: str
    value: str | None = None
    sort_order: int = Field(0, alias="sortOrder")
    description: str | None = None
    model_config = {"populate_by_name": True}
