from app.database import get_pool


class PostCommandRepository:
    async def insert_post(self, board_id: str, title: str, content: str | None, created_by: str) -> int:
        pool = get_pool()
        return await pool.fetchval(
            """
            INSERT INTO tb_post (board_id, title, content, created_by, modified_by, created_date, modified_date)
            VALUES ($1, $2, $3, $4, $4, NOW(), NOW())
            RETURNING post_id
            """,
            board_id, title, content, created_by,
        )

    async def update_post(self, post_id: int, title: str, content: str | None, modified_by: str):
        pool = get_pool()
        await pool.execute(
            """
            UPDATE tb_post
               SET title = $1, content = $2, modified_by = $3, modified_date = NOW()
             WHERE post_id = $4
            """,
            title, content, modified_by, post_id,
        )

    async def delete_post(self, post_id: int):
        pool = get_pool()
        await pool.execute("DELETE FROM tb_post WHERE post_id = $1", post_id)

    async def update_view_count(self, post_id: int):
        pool = get_pool()
        await pool.execute(
            "UPDATE tb_post SET view_count = view_count + 1 WHERE post_id = $1",
            post_id,
        )

    async def insert_post_file(self, post_id: int, file_id: str):
        pool = get_pool()
        await pool.execute(
            "INSERT INTO tb_post_file (post_id, file_id) VALUES ($1, $2)",
            post_id, file_id,
        )

    async def delete_post_files(self, post_id: int):
        pool = get_pool()
        await pool.execute("DELETE FROM tb_post_file WHERE post_id = $1", post_id)
