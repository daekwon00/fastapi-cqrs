from pydantic import Field

from app.common.schemas import CamelModel


class PositionRoleResponse(CamelModel):
    position_id: str = Field(alias="positionId")
    position_name: str = Field(alias="positionName")
    role_ids: list[str] = Field(alias="roleIds")


class UpdatePositionRoleRequest(CamelModel):
    role_ids: list[str] = Field(alias="roleIds")
