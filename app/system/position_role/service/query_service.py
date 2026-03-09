from app.system.position_role.repository.query_repository import PositionRoleQueryRepository
from app.system.position_role.schemas import PositionRoleResponse


class PositionRoleQueryService:
    def __init__(self):
        self.repo = PositionRoleQueryRepository()

    async def get_all_position_roles(self) -> list[PositionRoleResponse]:
        rows = await self.repo.select_all_position_roles()
        grouped: dict[str, PositionRoleResponse] = {}
        for r in rows:
            pid = r["position_id"]
            if pid not in grouped:
                grouped[pid] = PositionRoleResponse(
                    positionId=pid, positionName=r["position_name"], roleIds=[],
                )
            if r["role_id"]:
                grouped[pid].role_ids.append(r["role_id"])
        return list(grouped.values())
