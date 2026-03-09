import asyncpg

from app.database import get_pool


class PositionRoleQueryRepository:
    async def select_all_position_roles(self) -> list[asyncpg.Record]:
        return await get_pool().fetch(
            """SELECT p.position_id, p.position_name, pr.role_id
                 FROM tb_position p
                 LEFT JOIN tb_position_role pr ON p.position_id = pr.position_id
                WHERE p.use_yn = true
                ORDER BY p.position_level, pr.role_id"""
        )
