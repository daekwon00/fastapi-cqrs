from app.database import get_pool


class FileCommandRepository:
    async def insert_file(
        self,
        file_id: str,
        original_filename: str,
        stored_filename: str,
        file_path: str,
        file_size: int,
        content_type: str | None,
        created_by: str,
    ):
        pool = get_pool()
        await pool.execute(
            """
            INSERT INTO tb_file (file_id, original_filename, stored_filename, file_path,
                                 file_size, content_type, created_by, created_date, modified_date)
            VALUES ($1, $2, $3, $4, $5, $6, $7, NOW(), NOW())
            """,
            file_id, original_filename, stored_filename, file_path,
            file_size, content_type, created_by,
        )
