import asyncpg

from app.database import get_pool


class AdminDashboardQueryRepository:
    async def select_total_users(self) -> int:
        return await get_pool().fetchval("SELECT COUNT(*) FROM tb_user")

    async def select_today_registered(self) -> int:
        return await get_pool().fetchval("SELECT COUNT(*) FROM tb_user WHERE created_date >= CURRENT_DATE")

    async def select_active_boards(self) -> int:
        return await get_pool().fetchval("SELECT COUNT(*) FROM tb_board WHERE use_yn = true")

    async def select_today_posts(self) -> int:
        return await get_pool().fetchval("SELECT COUNT(*) FROM tb_post WHERE created_date >= CURRENT_DATE")

    async def select_recent_users(self) -> list[asyncpg.Record]:
        return await get_pool().fetch(
            "SELECT user_id, user_name, email, created_date FROM tb_user ORDER BY created_date DESC LIMIT 5"
        )
