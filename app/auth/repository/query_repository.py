import asyncpg

from app.database import get_pool


class AuthQueryRepository:
    async def select_user_by_id(self, user_id: str) -> asyncpg.Record | None:
        pool = get_pool()
        return await pool.fetchrow(
            """
            SELECT user_id, user_name, password, email, phone,
                   department, position_id, is_active, last_login_date, created_date
              FROM tb_user
             WHERE user_id = $1
            """,
            user_id,
        )

    async def select_roles_by_user_id(self, user_id: str) -> list[str]:
        pool = get_pool()
        rows = await pool.fetch(
            "SELECT role_id FROM tb_user_role WHERE user_id = $1",
            user_id,
        )
        return [row["role_id"] for row in rows]

    async def exists_by_user_id(self, user_id: str) -> bool:
        pool = get_pool()
        return await pool.fetchval(
            "SELECT EXISTS(SELECT 1 FROM tb_user WHERE user_id = $1)",
            user_id,
        )
