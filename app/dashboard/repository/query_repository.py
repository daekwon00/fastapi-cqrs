import asyncpg

from app.database import get_pool


class DashboardQueryRepository:
    async def select_total_posts(self) -> int:
        pool = get_pool()
        return await pool.fetchval("SELECT COUNT(*) FROM tb_post")

    async def select_today_posts(self) -> int:
        pool = get_pool()
        return await pool.fetchval("SELECT COUNT(*) FROM tb_post WHERE created_date >= CURRENT_DATE")

    async def select_total_users(self) -> int:
        pool = get_pool()
        return await pool.fetchval("SELECT COUNT(*) FROM tb_user WHERE is_active = true")

    async def select_my_posts(self, user_id: str) -> int:
        pool = get_pool()
        return await pool.fetchval("SELECT COUNT(*) FROM tb_post WHERE created_by = $1", user_id)

    async def select_chart_data(self, days: int) -> list[asyncpg.Record]:
        pool = get_pool()
        return await pool.fetch(
            """
            SELECT TO_CHAR(d.date, 'FMMM/FMDD') AS date,
                   COALESCE(COUNT(p.post_id), 0) AS count
              FROM (
                  SELECT CURRENT_DATE - generate_series(0, $1 - 1) AS date
              ) d
              LEFT JOIN tb_post p
                  ON p.created_date >= d.date
                 AND p.created_date < d.date + INTERVAL '1 day'
             GROUP BY d.date
             ORDER BY d.date
            """,
            days,
        )
