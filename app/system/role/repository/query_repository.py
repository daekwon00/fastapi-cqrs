import asyncpg

from app.database import get_pool


class RoleQueryRepository:
    async def select_role_list(self) -> list[asyncpg.Record]:
        return await get_pool().fetch(
            "SELECT role_id AS id, role_name AS name, description FROM tb_role WHERE use_yn = true ORDER BY role_level"
        )

    async def select_role_by_id(self, role_id: str) -> asyncpg.Record | None:
        return await get_pool().fetchrow(
            "SELECT role_id AS id, role_name AS name, description FROM tb_role WHERE role_id = $1", role_id
        )
