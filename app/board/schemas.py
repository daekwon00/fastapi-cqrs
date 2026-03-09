from datetime import datetime

from pydantic import BaseModel, Field


# Board
class BoardResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    is_active: bool = Field(alias="isActive")
    post_count: int = Field(alias="postCount")

    model_config = {"populate_by_name": True}


# Post - Request
class CreatePostRequest(BaseModel):
    board_id: str = Field(..., alias="boardId", description="게시판 ID")
    title: str = Field(..., min_length=1, description="제목")
    content: str | None = Field(None, description="내용")
    file_ids: list[str] | None = Field(None, alias="fileIds", description="첨부파일 ID 목록")


class UpdatePostRequest(BaseModel):
    title: str = Field(..., min_length=1, description="제목")
    content: str | None = Field(None, description="내용")
    file_ids: list[str] | None = Field(None, alias="fileIds", description="첨부파일 ID 목록")


# Post - Response
class PostListResponse(BaseModel):
    id: int
    board_id: str = Field(alias="boardId")
    title: str
    author_name: str | None = Field(None, alias="authorName")
    view_count: int = Field(alias="viewCount")
    created_at: datetime | None = Field(None, alias="createdAt")
    updated_at: datetime | None = Field(None, alias="updatedAt")

    model_config = {"populate_by_name": True}


class AuthorResponse(BaseModel):
    id: str
    username: str
    name: str
    email: str | None = None
    role: str = "USER"


class FileInfoResponse(BaseModel):
    id: str
    original_name: str = Field(alias="originalName")
    stored_name: str = Field(alias="storedName")
    size: int
    content_type: str | None = Field(None, alias="contentType")

    model_config = {"populate_by_name": True}


class PostResponse(BaseModel):
    id: int
    board_id: str = Field(alias="boardId")
    title: str
    content: str | None = None
    author: AuthorResponse
    view_count: int = Field(alias="viewCount")
    files: list[FileInfoResponse] = []
    created_at: datetime | None = Field(None, alias="createdAt")
    updated_at: datetime | None = Field(None, alias="updatedAt")

    model_config = {"populate_by_name": True}
