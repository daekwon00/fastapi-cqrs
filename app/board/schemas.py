from datetime import datetime

from pydantic import BaseModel, Field

from app.common.schemas import CamelModel


# Board
class BoardResponse(CamelModel):
    id: str
    name: str
    description: str | None = None
    is_active: bool = Field(alias="isActive")
    post_count: int = Field(alias="postCount")


# Post - Request
class CreatePostRequest(CamelModel):
    board_id: str = Field(..., alias="boardId", description="게시판 ID")
    title: str = Field(..., min_length=1, description="제목")
    content: str | None = Field(None, description="내용")
    file_ids: list[str] | None = Field(None, alias="fileIds", description="첨부파일 ID 목록")


class UpdatePostRequest(CamelModel):
    title: str = Field(..., min_length=1, description="제목")
    content: str | None = Field(None, description="내용")
    file_ids: list[str] | None = Field(None, alias="fileIds", description="첨부파일 ID 목록")


# Post - Response
class PostListResponse(CamelModel):
    id: int
    board_id: str = Field(alias="boardId")
    title: str
    author_name: str | None = Field(None, alias="authorName")
    view_count: int = Field(alias="viewCount")
    created_at: datetime | None = Field(None, alias="createdAt")
    updated_at: datetime | None = Field(None, alias="updatedAt")


class AuthorResponse(BaseModel):
    id: str
    username: str
    name: str
    email: str | None = None
    role: str = "USER"


class FileInfoResponse(CamelModel):
    id: str
    original_name: str = Field(alias="originalName")
    stored_name: str = Field(alias="storedName")
    size: int
    content_type: str | None = Field(None, alias="contentType")


class PostResponse(CamelModel):
    id: int
    board_id: str = Field(alias="boardId")
    title: str
    content: str | None = None
    author: AuthorResponse
    view_count: int = Field(alias="viewCount")
    files: list[FileInfoResponse] = []
    created_at: datetime | None = Field(None, alias="createdAt")
    updated_at: datetime | None = Field(None, alias="updatedAt")
