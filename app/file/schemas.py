from pydantic import Field

from app.common.schemas import CamelModel


class FileResponse(CamelModel):
    id: str
    original_name: str = Field(alias="originalName")
    stored_name: str = Field(alias="storedName")
    size: int
    content_type: str | None = Field(None, alias="contentType")
