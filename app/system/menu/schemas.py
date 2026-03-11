from pydantic import BaseModel, Field


class MenuResponse(BaseModel):
    id: str
    name: str
    path: str | None = None
    icon: str | None = None
    parent_id: str | None = Field(None, alias="parentId")
    sort_order: int = Field(alias="sortOrder")
    is_active: bool = Field(alias="isActive")
    children: list["MenuResponse"] = []
    model_config = {"populate_by_name": True}


class MyMenusResponse(BaseModel):
    menus: list[MenuResponse]
    admin_menus: list[MenuResponse] = Field(default_factory=list, alias="adminMenus")
    model_config = {"populate_by_name": True}


class CreateMenuRequest(BaseModel):
    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    path: str | None = None
    icon: str | None = None
    parent_id: str | None = Field(None, alias="parentId")
    sort_order: int = Field(0, alias="sortOrder")


class UpdateMenuRequest(BaseModel):
    name: str = Field(..., min_length=1)
    path: str | None = None
    icon: str | None = None
    parent_id: str | None = Field(None, alias="parentId")
    sort_order: int = Field(0, alias="sortOrder")
