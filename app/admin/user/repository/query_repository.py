import asyncpg

from app.database import get_pool


class AdminUserQueryRepository:
    async def select_user_list(self, search: str | None, limit: int, offset: int) -> list[asyncpg.Record]:
        pool = get_pool()
        query = """
            SELECT u.user_id, u.user_name, u.email, u.phone,
                   u.department, u.is_active, u.last_login_date, u.created_date,
                   ur.role_id,
                   cc.code_name AS position_name
              FROM tb_user u
              LEFT JOIN tb_user_role ur ON u.user_id = ur.user_id
              LEFT JOIN tb_role r ON ur.role_id = r.role_id
              LEFT JOIN tb_common_code cc ON u.position_id = cc.code_id AND cc.code_group_id = 'POSITION'
             WHERE 1=1
        """
        params: list = []
        idx = 1
        if search:
            query += f" AND (u.user_name LIKE ${idx} OR u.email LIKE ${idx})"
            params.append(f"%{search}%")
            idx += 1
        query += f" ORDER BY u.created_date DESC LIMIT ${idx} OFFSET ${idx + 1}"
        params.extend([limit, offset])
        return await pool.fetch(query, *params)

    async def select_user_count(self, search: str | None) -> int:
        pool = get_pool()
        query = "SELECT COUNT(*) FROM tb_user u WHERE 1=1"
        params: list = []
        if search:
            query += " AND (u.user_name LIKE $1 OR u.email LIKE $1)"
            params.append(f"%{search}%")
        return await pool.fetchval(query, *params)

    async def select_user_by_id(self, user_id: str) -> asyncpg.Record | None:
        pool = get_pool()
        return await pool.fetchrow(
            """
            SELECT u.user_id, u.user_name, u.email, u.phone,
                   u.department, u.is_active, u.last_login_date, u.created_date,
                   ur.role_id,
                   cc.code_name AS position_name
              FROM tb_user u
              LEFT JOIN tb_user_role ur ON u.user_id = ur.user_id
              LEFT JOIN tb_role r ON ur.role_id = r.role_id
              LEFT JOIN tb_common_code cc ON u.position_id = cc.code_id AND cc.code_group_id = 'POSITION'
             WHERE u.user_id = $1
            """,
            user_id,
        )
