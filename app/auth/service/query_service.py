import asyncpg

from app.auth.repository.query_repository import AuthQueryRepository


class AuthQueryService:
    def __init__(self):
        self.repo = AuthQueryRepository()

    async def get_user_by_id(self, user_id: str) -> asyncpg.Record | None:
        return await self.repo.select_user_by_id(user_id)

    async def get_roles_by_user_id(self, user_id: str) -> list[str]:
        return await self.repo.select_roles_by_user_id(user_id)

    async def exists_by_user_id(self, user_id: str) -> bool:
        return await self.repo.exists_by_user_id(user_id)
