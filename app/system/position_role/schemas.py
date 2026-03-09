from pydantic import BaseModel, Field


class PositionRoleResponse(BaseModel):
    position_id: str = Field(alias="positionId")
    position_name: str = Field(alias="positionName")
    role_ids: list[str] = Field(alias="roleIds")
    model_config = {"populate_by_name": True}


class UpdatePositionRoleRequest(BaseModel):
    role_ids: list[str] = Field(alias="roleIds")
    model_config = {"populate_by_name": True}
