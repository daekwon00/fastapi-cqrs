from pydantic import BaseModel, Field

from app.common.schemas import CamelModel


class AdminBoardResponse(CamelModel):
    id: str
    name: str
    description: str | None = None
    is_active: bool = Field(alias="isActive")
    post_count: int = Field(alias="postCount")


class CreateBoardRequest(BaseModel):
    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    description: str | None = None


class UpdateBoardRequest(BaseModel):
    name: str = Field(..., min_length=1)
    description: str | None = None
