import asyncpg

from app.database import get_pool

BOARD_LIST_SQL = """
    SELECT b.board_id AS id, b.board_name AS name, b.description,
           b.use_yn AS is_active, COALESCE(pc.cnt, 0) AS post_count
      FROM tb_board b
      LEFT JOIN (SELECT board_id, COUNT(*) AS cnt FROM tb_post GROUP BY board_id) pc
        ON b.board_id = pc.board_id
"""


class AdminBoardQueryRepository:
    async def select_board_list(self) -> list[asyncpg.Record]:
        pool = get_pool()
        return await pool.fetch(BOARD_LIST_SQL + " ORDER BY b.created_date")

    async def select_board_by_id(self, board_id: str) -> asyncpg.Record | None:
        pool = get_pool()
        return await pool.fetchrow(BOARD_LIST_SQL + " WHERE b.board_id = $1", board_id)
