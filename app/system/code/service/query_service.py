from app.system.code.repository.query_repository import CodeQueryRepository
from app.system.code.schemas import CodeGroupResponse, CodeResponse


class CodeQueryService:
    def __init__(self):
        self.repo = CodeQueryRepository()

    async def get_code_group_list(self) -> list[CodeGroupResponse]:
        rows = await self.repo.select_code_group_list()
        return [CodeGroupResponse(id=r["id"], name=r["name"], description=r["description"],
                                  isActive=bool(r["is_active"])) for r in rows]

    async def get_code_list(self, group_code: str | None = None) -> list[CodeResponse]:
        rows = await self.repo.select_code_list(group_code)
        return [self._to_response(r) for r in rows]

    async def get_code_by_id(self, code_id: str) -> CodeResponse | None:
        r = await self.repo.select_code_by_id(code_id)
        return self._to_response(r) if r else None

    @staticmethod
    def _to_response(r) -> CodeResponse:
        return CodeResponse(
            id=r["code_id"], groupCode=r["code_group_id"], code=r["code"],
            name=r["code_name"], value=r["code_value"],
            sortOrder=r["sort_order"], isActive=bool(r["use_yn"]),
            description=r["description"],
        )
