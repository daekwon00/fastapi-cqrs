from app.database import get_pool


class AdminUserCommandRepository:
    async def insert_user(self, user_id: str, user_name: str, password: str, email: str, department: str | None):
        pool = get_pool()
        await pool.execute(
            "INSERT INTO tb_user (user_id, user_name, password, email, department) VALUES ($1, $2, $3, $4, $5)",
            user_id, user_name, password, email, department,
        )

    async def insert_user_role(self, user_id: str, role_id: str):
        pool = get_pool()
        await pool.execute(
            "INSERT INTO tb_user_role (user_id, role_id) VALUES ($1, $2)",
            user_id, role_id,
        )

    async def update_user(self, user_id: str, user_name: str, email: str, department: str | None):
        pool = get_pool()
        await pool.execute(
            """
            UPDATE tb_user SET user_name = $1, email = $2, department = $3, modified_date = CURRENT_TIMESTAMP
             WHERE user_id = $4
            """,
            user_name, email, department, user_id,
        )

    async def delete_user_roles(self, user_id: str):
        pool = get_pool()
        await pool.execute("DELETE FROM tb_user_role WHERE user_id = $1", user_id)

    async def toggle_active(self, user_id: str):
        pool = get_pool()
        await pool.execute(
            "UPDATE tb_user SET is_active = NOT is_active, modified_date = CURRENT_TIMESTAMP WHERE user_id = $1",
            user_id,
        )
