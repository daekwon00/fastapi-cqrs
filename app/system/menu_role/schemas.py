from pydantic import Field

from app.common.schemas import CamelModel


class MenuRoleResponse(CamelModel):
    menu_id: str = Field(alias="menuId")
    role_id: str = Field(alias="roleId")


class UpdateMenuRoleRequest(CamelModel):
    menu_ids: list[str] = Field(alias="menuIds")
