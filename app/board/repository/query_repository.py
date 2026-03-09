import asyncpg

from app.common.pagination import SortOrder
from app.database import get_pool

SORT_ORDER_WHITELIST = {"ASC", "DESC"}


class BoardQueryRepository:
    async def select_board_list(self) -> list[asyncpg.Record]:
        pool = get_pool()
        return await pool.fetch(
            """
            SELECT b.board_id    AS id,
                   b.board_name  AS name,
                   b.description,
                   b.use_yn      AS is_active,
                   COALESCE(pc.cnt, 0) AS post_count
              FROM tb_board b
              LEFT JOIN (
                  SELECT board_id, COUNT(*) AS cnt
                    FROM tb_post
                   GROUP BY board_id
              ) pc ON pc.board_id = b.board_id
             WHERE b.use_yn = true
             ORDER BY b.created_date
            """
        )

    async def select_board_by_id(self, board_id: str) -> asyncpg.Record | None:
        pool = get_pool()
        return await pool.fetchrow(
            """
            SELECT b.board_id    AS id,
                   b.board_name  AS name,
                   b.description,
                   b.use_yn      AS is_active,
                   COALESCE(pc.cnt, 0) AS post_count
              FROM tb_board b
              LEFT JOIN (
                  SELECT board_id, COUNT(*) AS cnt
                    FROM tb_post
                   GROUP BY board_id
              ) pc ON pc.board_id = b.board_id
             WHERE b.board_id = $1
            """,
            board_id,
        )


class PostQueryRepository:
    async def select_post_list(
        self,
        board_id: str,
        search: str | None,
        search_type: str | None,
        sort_order: SortOrder,
        limit: int,
        offset: int,
    ) -> list[asyncpg.Record]:
        pool = get_pool()
        query, params = self._build_search_query(
            """
            SELECT p.post_id       AS id,
                   p.board_id,
                   p.title,
                   u.user_name     AS author_name,
                   p.view_count,
                   p.created_date  AS created_at,
                   p.modified_date AS updated_at
              FROM tb_post p
              LEFT JOIN tb_user u ON u.user_id = p.created_by
             WHERE p.board_id = $1
            """,
            board_id, search, search_type, param_offset=1,
        )
        # 정렬 (화이트리스트 검증)
        order = sort_order.value if sort_order.value in SORT_ORDER_WHITELIST else "DESC"
        query += f" ORDER BY p.created_date {order}"
        query += f" LIMIT ${len(params) + 1} OFFSET ${len(params) + 2}"
        params.extend([limit, offset])
        return await pool.fetch(query, *params)

    async def select_post_count(
        self,
        board_id: str,
        search: str | None,
        search_type: str | None,
    ) -> int:
        pool = get_pool()
        query, params = self._build_search_query(
            """
            SELECT COUNT(*)
              FROM tb_post p
              LEFT JOIN tb_user u ON u.user_id = p.created_by
             WHERE p.board_id = $1
            """,
            board_id, search, search_type, param_offset=1,
        )
        return await pool.fetchval(query, *params)

    async def select_post_by_id(self, post_id: int) -> asyncpg.Record | None:
        pool = get_pool()
        return await pool.fetchrow(
            """
            SELECT p.post_id       AS id,
                   p.board_id,
                   p.title,
                   p.content,
                   p.view_count,
                   p.created_by,
                   p.created_date,
                   p.modified_date,
                   u.user_id       AS author_id,
                   u.user_name     AS author_name,
                   u.email         AS author_email
              FROM tb_post p
              LEFT JOIN tb_user u ON u.user_id = p.created_by
             WHERE p.post_id = $1
            """,
            post_id,
        )

    async def select_post_files(self, post_id: int) -> list[asyncpg.Record]:
        pool = get_pool()
        return await pool.fetch(
            """
            SELECT f.file_id           AS id,
                   f.original_filename  AS original_name,
                   f.stored_filename    AS stored_name,
                   f.file_size          AS size,
                   f.content_type
              FROM tb_post_file pf
              JOIN tb_file f ON f.file_id = pf.file_id
             WHERE pf.post_id = $1
            """,
            post_id,
        )

    async def select_recent_posts(self) -> list[asyncpg.Record]:
        pool = get_pool()
        return await pool.fetch(
            """
            SELECT p.post_id       AS id,
                   p.board_id,
                   p.title,
                   u.user_name     AS author_name,
                   p.view_count,
                   p.created_date  AS created_at,
                   p.modified_date AS updated_at
              FROM tb_post p
              LEFT JOIN tb_user u ON u.user_id = p.created_by
             ORDER BY p.created_date DESC
             LIMIT 5
            """
        )

    def _build_search_query(
        self,
        base_query: str,
        board_id: str,
        search: str | None,
        search_type: str | None,
        param_offset: int,
    ) -> tuple[str, list]:
        params: list = [board_id]
        idx = param_offset + 1  # 다음 파라미터 인덱스

        if search:
            like_param = f"%{search}%"
            if search_type == "title":
                base_query += f" AND p.title LIKE ${idx}"
                params.append(like_param)
            elif search_type == "author":
                base_query += f" AND u.user_name LIKE ${idx}"
                params.append(like_param)
            else:  # all
                base_query += f" AND (p.title LIKE ${idx} OR u.user_name LIKE ${idx})"
                params.append(like_param)

        return base_query, params
