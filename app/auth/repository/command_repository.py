from app.database import get_pool


class AuthCommandRepository:
    async def insert_user(self, user_id: str, user_name: str, password: str, email: str):
        pool = get_pool()
        await pool.execute(
            """
            INSERT INTO tb_user (user_id, user_name, password, email, created_date, modified_date)
            VALUES ($1, $2, $3, $4, NOW(), NOW())
            """,
            user_id, user_name, password, email,
        )

    async def insert_user_role(self, user_id: str, role_id: str):
        pool = get_pool()
        await pool.execute(
            """
            INSERT INTO tb_user_role (user_id, role_id, created_by, created_date)
            VALUES ($1, $2, $1, NOW())
            """,
            user_id, role_id,
        )

    async def update_last_login_date(self, user_id: str):
        pool = get_pool()
        await pool.execute(
            "UPDATE tb_user SET last_login_date = NOW() WHERE user_id = $1",
            user_id,
        )

    async def insert_login_history(
        self, user_id: str, login_ip: str, login_success: bool, login_fail_reason: str | None
    ):
        pool = get_pool()
        await pool.execute(
            """
            INSERT INTO tb_login_history (user_id, login_ip, login_success, login_fail_reason, login_date)
            VALUES ($1, $2, $3, $4, NOW())
            """,
            user_id, login_ip, login_success, login_fail_reason,
        )
