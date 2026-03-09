from app.common.exceptions import NotFoundException
from app.system.role.repository.query_repository import RoleQueryRepository
from app.system.role.schemas import RoleResponse


class RoleQueryService:
    def __init__(self):
        self.repo = RoleQueryRepository()

    async def get_role_list(self) -> list[RoleResponse]:
        rows = await self.repo.select_role_list()
        return [RoleResponse(**dict(r)) for r in rows]

    async def get_role_by_id(self, role_id: str) -> RoleResponse:
        row = await self.repo.select_role_by_id(role_id)
        if row is None:
            raise NotFoundException("역할을 찾을 수 없습니다.")
        return RoleResponse(**dict(row))
