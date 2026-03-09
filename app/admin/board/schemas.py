from pydantic import BaseModel, Field


class AdminBoardResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    is_active: bool = Field(alias="isActive")
    post_count: int = Field(alias="postCount")
    model_config = {"populate_by_name": True}


class CreateBoardRequest(BaseModel):
    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    description: str | None = None


class UpdateBoardRequest(BaseModel):
    name: str = Field(..., min_length=1)
    description: str | None = None
