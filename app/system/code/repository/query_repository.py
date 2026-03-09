import asyncpg

from app.database import get_pool


class CodeQueryRepository:
    async def select_code_group_list(self) -> list[asyncpg.Record]:
        return await get_pool().fetch(
            """SELECT code_group_id AS id, code_group_name AS name, description, use_yn AS is_active
                 FROM tb_common_code_group
                ORDER BY code_group_id"""
        )

    async def select_code_list(self, group_code: str | None = None) -> list[asyncpg.Record]:
        if group_code:
            return await get_pool().fetch(
                """SELECT code_id, code_group_id, code_id AS code, code_name, code_value,
                          COALESCE(sort_order, 0) AS sort_order, use_yn, description
                     FROM tb_common_code
                    WHERE code_group_id = $1
                    ORDER BY code_group_id, sort_order""",
                group_code,
            )
        return await get_pool().fetch(
            """SELECT code_id, code_group_id, code_id AS code, code_name, code_value,
                      COALESCE(sort_order, 0) AS sort_order, use_yn, description
                 FROM tb_common_code
                ORDER BY code_group_id, sort_order"""
        )

    async def select_code_by_id(self, code_id: str) -> asyncpg.Record | None:
        return await get_pool().fetchrow(
            """SELECT code_id, code_group_id, code_id AS code, code_name, code_value,
                      COALESCE(sort_order, 0) AS sort_order, use_yn, description
                 FROM tb_common_code
                WHERE code_id = $1""",
            code_id,
        )
