import asyncpg

from app.database import get_pool


class MenuRoleQueryRepository:
    async def select_all_menu_roles(self) -> list[asyncpg.Record]:
        return await get_pool().fetch(
            """SELECT menu_id, role_id
                 FROM tb_role_menu
                ORDER BY role_id, menu_id"""
        )
