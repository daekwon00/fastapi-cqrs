from pydantic import BaseModel, Field


class MenuRoleResponse(BaseModel):
    menu_id: str = Field(alias="menuId")
    role_id: str = Field(alias="roleId")
    model_config = {"populate_by_name": True}


class UpdateMenuRoleRequest(BaseModel):
    menu_ids: list[str] = Field(alias="menuIds")
    model_config = {"populate_by_name": True}
