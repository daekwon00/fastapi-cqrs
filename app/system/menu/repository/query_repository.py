import asyncpg

from app.database import get_pool


class MenuQueryRepository:
    async def select_all_menus(self) -> list[asyncpg.Record]:
        return await get_pool().fetch(
            """SELECT menu_id, parent_menu_id, menu_name, menu_url, menu_icon, sort_order, use_yn
                 FROM tb_menu WHERE use_yn = true ORDER BY sort_order"""
        )

    async def select_menus_by_role_ids(self, role_ids: list[str]) -> list[asyncpg.Record]:
        return await get_pool().fetch(
            """SELECT DISTINCT m.menu_id, m.parent_menu_id, m.menu_name, m.menu_url, m.menu_icon, m.sort_order, m.use_yn
                 FROM tb_menu m
                 INNER JOIN tb_role_menu rm ON m.menu_id = rm.menu_id
                WHERE m.use_yn = true AND rm.role_id = ANY($1::text[])
                ORDER BY m.sort_order""",
            role_ids,
        )
