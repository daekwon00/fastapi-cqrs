from app.database import get_pool


class UserCommandRepository:
    async def update_profile(self, user_id: str, user_name: str, email: str, phone: str | None):
        pool = get_pool()
        await pool.execute(
            """
            UPDATE tb_user
               SET user_name = $1, email = $2, phone = $3, modified_date = NOW()
             WHERE user_id = $4
            """,
            user_name, email, phone, user_id,
        )

    async def update_password(self, user_id: str, new_password: str):
        pool = get_pool()
        await pool.execute(
            """
            UPDATE tb_user
               SET password = $1, modified_date = NOW()
             WHERE user_id = $2
            """,
            new_password, user_id,
        )
