import asyncpg

from app.database import get_pool


class UserQueryRepository:
    async def select_user_profile(self, user_id: str) -> asyncpg.Record | None:
        pool = get_pool()
        return await pool.fetchrow(
            """
            SELECT u.user_id     AS id,
                   u.user_id     AS username,
                   u.user_name   AS name,
                   u.email,
                   u.phone,
                   u.department,
                   COALESCE(cc.code_name, u.position_id) AS position,
                   CASE WHEN EXISTS (
                       SELECT 1 FROM tb_user_role ur
                       WHERE ur.user_id = u.user_id
                         AND ur.role_id IN ('ROLE_SUPER_ADMIN', 'ROLE_ADMIN')
                   ) THEN 'ADMIN' ELSE 'USER' END AS role,
                   u.created_date AS created_at
              FROM tb_user u
              LEFT JOIN tb_common_code cc ON cc.code_id = u.position_id
             WHERE u.user_id = $1
            """,
            user_id,
        )
