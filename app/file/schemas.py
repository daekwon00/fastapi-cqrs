from pydantic import BaseModel, Field


class FileResponse(BaseModel):
    id: str
    original_name: str = Field(alias="originalName")
    stored_name: str = Field(alias="storedName")
    size: int
    content_type: str | None = Field(None, alias="contentType")

    model_config = {"populate_by_name": True}
