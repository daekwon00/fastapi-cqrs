from app.admin.user.repository.query_repository import AdminUserQueryRepository
from app.admin.user.schemas import AdminUserResponse
from app.common.exceptions import NotFoundException


class AdminUserQueryService:
    def __init__(self):
        self.repo = AdminUserQueryRepository()

    async def get_user_list(self, search: str | None, limit: int, offset: int) -> list[AdminUserResponse]:
        rows = await self.repo.select_user_list(search, limit, offset)
        return [self._to_response(row) for row in rows]

    async def get_user_count(self, search: str | None) -> int:
        return await self.repo.select_user_count(search)

    async def get_user_by_id(self, user_id: str) -> AdminUserResponse:
        row = await self.repo.select_user_by_id(user_id)
        if row is None:
            raise NotFoundException("사용자를 찾을 수 없습니다.")
        return self._to_response(row)

    def _to_response(self, row) -> AdminUserResponse:
        role_id = row["role_id"]
        role = "ADMIN" if role_id and "ADMIN" in role_id else "USER"
        return AdminUserResponse(
            id=row["user_id"], username=row["user_id"], name=row["user_name"],
            email=row["email"], phone=row["phone"], role=role,
            department=row["department"], position=row["position_name"],
            createdAt=str(row["created_date"]) if row["created_date"] else None,
            isActive=bool(row["is_active"]),
            lastLoginAt=str(row["last_login_date"]) if row["last_login_date"] else None,
        )
