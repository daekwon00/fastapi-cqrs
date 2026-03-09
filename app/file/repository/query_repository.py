import asyncpg

from app.database import get_pool


class FileQueryRepository:
    async def select_file_by_id(self, file_id: str) -> asyncpg.Record | None:
        pool = get_pool()
        return await pool.fetchrow(
            """
            SELECT file_id           AS id,
                   original_filename AS original_name,
                   stored_filename   AS stored_name,
                   file_path,
                   file_size         AS size,
                   content_type
              FROM tb_file
             WHERE file_id = $1
            """,
            file_id,
        )
