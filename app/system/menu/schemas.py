from pydantic import Field

from app.common.schemas import CamelModel


class MenuResponse(CamelModel):
    id: str
    name: str
    path: str | None = None
    icon: str | None = None
    parent_id: str | None = Field(None, alias="parentId")
    sort_order: int = Field(alias="sortOrder")
    is_active: bool = Field(alias="isActive")
    children: list["MenuResponse"] = []


class MyMenusResponse(CamelModel):
    menus: list[MenuResponse]
    admin_menus: list[MenuResponse] = Field(default_factory=list, alias="adminMenus")


class CreateMenuRequest(CamelModel):
    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    path: str | None = None
    icon: str | None = None
    parent_id: str | None = Field(None, alias="parentId")
    sort_order: int = Field(0, alias="sortOrder")


class UpdateMenuRequest(CamelModel):
    name: str = Field(..., min_length=1)
    path: str | None = None
    icon: str | None = None
    parent_id: str | None = Field(None, alias="parentId")
    sort_order: int = Field(0, alias="sortOrder")
